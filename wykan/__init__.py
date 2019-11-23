import requests
from requests.exceptions import HTTPError

from .exceptions import WekanException
from .models.board import Board
from .models.user import User


class Wykan:
    verify_tls = True  # Set to False before initialization to ignore TLS validity.

    def __init__(self, wekan_url: str, username: str, password: str):
        """
        Initialize a connection to a Wekan server.
        This object logs on to the Wekan server and lets you control it using REST API.

        :param wekan_url: Base url to the Wekan server. Example: https://mywekan.com/
        """

        self.wekan_url = wekan_url

        login_user = self.post("/users/login",
                               data={"username": username, "password": password},
                               authed=False)
        self.token = login_user["token"]
        self.user = User(self, login_user["id"])

    def get(self, url: str, **kwargs):
        return self._internal_api_call(url, "get", **kwargs)

    def post(self, url: str, data: dict, **kwargs):
        return self._internal_api_call(url, "post", data, **kwargs)

    def delete(self, url: str, **kwargs):
        return self._internal_api_call(url, "delete", **kwargs)

    def put(self, url: str, data: dict, **kwargs):
        return self._internal_api_call(url, "put", data, **kwargs)

    def _internal_api_call(self, rest_url: str, method: str, data: dict = None, **kwargs) -> dict:
        """
        Issues the actual request to the Wekan server.

        :param rest_url: example: /users/login
        :param method: Type of REST method to send.
        :param data: Dictionary to be sent in the request.
        :param authed: Should the request be sent with authorization token.
        :return: JSON encoded REST response.
        """

        request_url = f"{self.wekan_url}{rest_url}"

        headers = dict()
        request_data = dict()

        # Some api requests do not require authorization.
        if kwargs.get("authed", True):
            headers["Authorization"] = f"Bearer {self.token}"

        # Except for the initial login request.
        if rest_url == "/users/login":
            headers["Content-type"] = "application/x-www-form-urlencoded"
            request_data["data"] = data

        api_response = requests.request(method, request_url,
                                        headers=headers,
                                        json=data,
                                        verify=Wykan.verify_tls,
                                        **request_data)

        # Check if the HTTP request returned successfully.
        if not api_response.ok:
            raise HTTPError(api_response.content.decode('utf-8'))

        response_json = dict()
        # Response might be valid, but return not content.
        if not api_response.content:
            return response_json

        response_json = api_response.json()

        # Check if the REST api request hasn't caused an error.
        if isinstance(response_json, dict) and "error" in response_json:
            raise WekanException(str(response_json))

        return response_json

    def get_user_boards(self, user_id: str) -> [Board]:
        """
        Get all the boards attached to a user.
        :param user_id: ID of the user.
        """

        user_boards = self.get(f"/api/users/{user_id}/boards")
        return [self.get_board(user_board["_id"]) for user_board in user_boards]

    def delete_board(self, board_id: str):
        """
        Delete a board.
        :param board_id: ID of the board to delete.
        """

        self.delete(f"/api/boards/{board_id}")

    def create_board(self, title: str, owner_id: str, **kwargs) -> Board:
        """
        Create a new board
        :param title: Name of the new board.
        :param owner_id: ID of the owner.
        :param is_admin: (optional) Is the owner an admin of the board.
        :param is_active: (optional) Is the board active.
        :param is_no_comments: (optional) Disable comments.
        :param is_comment_only: (optional) Enable comments only.
        :param permission: (optional) "private" board. Set to "public" for a public one.
        :param color: (optional) One of the allowed colors in :class:`BoardColors`
        """

        new_board_details = {
            "title": title,
            "owner": owner_id,
            "isAdmin": kwargs.get("is_admin", True),
            "isActive": kwargs.get("is_active", True),
            "isNoComments": kwargs.get("is_no_comments", False),
            "isCommentOnly": kwargs.get("is_comment_only", False),
            "permission": kwargs.get("permission", "private"),
            "color": kwargs.get("color")
        }

        new_board = self.post("/api/boards", new_board_details)
        return self.get_board(new_board["_id"])

    def get_board(self, id) -> Board:
        """
        Get a single board.
        :param id: ID of the board.
        """

        return Board(self, id)

    def get_public_boards(self) -> [Board]:
        """
        Return a list of all public boards.
        """

        public_boards = self.get("/api/boards")
        return [self.get_board(board_id["_id"]) for board_id in public_boards]

    def delete_user_by_username(self, username: str):
        """
        Delete a single user by username.
        USE WITH CAUTION. SEE: https://github.com/wekan/wekan/issues/1289
        :param username: Username of the user to delete.
        :return: id of the deleted user, None if the user doesn't exist.
        """

        user = self.get_user_by_username(username)
        if user is None:
            return

        return self.delete_user(user.id)

    def delete_user(self, id: str) -> str:
        """
        Delete a user.
        USE WITH CAUTION. SEE: https://github.com/wekan/wekan/issues/1289
        :param id: id of the user to delete
        :return: id of the deleted user.
        """

        deleted_user = self.delete(f"/api/users/{id}")
        return deleted_user["_id"]

    def create_new_user(self, username: str, email: str, password: str) -> User:
        """
        Create a new user.
        """

        new_user_details = {
            "username": username,
            "email": email,
            "password": password
        }

        new_user = self.post("/api/users", new_user_details)
        return self.get_user(new_user["_id"])

    def get_user_by_username(self, username) -> User:
        """
        Get a single user by username.
        :param username: Username to search by
        """

        users = self.get_all_users()
        for user in users:
            if user.username == username:
                return user

    def get_user(self, id) -> User:
        """
        Get a single user.
        :param id: ID of the user.
        """

        return User(self, id)

    def get_all_users(self) -> [User]:
        """
        Return a list of all the users.
        """

        all_users = self.get("/api/users")
        return [self.get_user(user_id["_id"]) for user_id in all_users]
