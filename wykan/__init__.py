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

    def _internal_api_call(self, rest_url: str, method: str, data: dict = None, **kwargs):
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

        # Some api requests do not require authorization.
        if kwargs.get("authed", True):
            headers["Authorization"] = f"Bearer {self.token}"

        # Every POST or PUT method sends JSON, thus requiring this header.
        if method in ("post", "put"):
            headers["Content-type"] = "application/json"

        # Except for the initial login request.
        if rest_url == "/users/login":
            headers["Content-type"] = "application/x-www-form-urlencoded"

        api_response = requests.request(method, request_url,
                                        data=data,
                                        headers=headers,
                                        verify=Wykan.verify_tls)

        # Check if the HTTP request returned successfully.
        if not api_response.ok:
            raise HTTPError(api_response.content.decode('utf-8'))

        response_json = api_response.json()

        # Check if the REST api request hasn't caused an error.
        if type(response_json) == dict and response_json.get("error"):
            raise WekanException(str(response_json))

        return response_json

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
        return new_user

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
