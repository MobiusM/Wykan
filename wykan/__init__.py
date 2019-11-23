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

        api_login = self.post("/users/login",
                              data={"username": username, "password": password},
                              authed=False)
        self.token = api_login["token"]
        self.user = User(self, api_login["id"], api_login)

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
        Does the actual request logic.

        :param rest_url: example: /users/login
        :param method: Type of REST method to send.
        :param data: Dictionary to be sent in the request.
        :param authed: Should the request be sent with authorization token.
        :return: JSON encoded REST response.
        """

        request_url = f"{self.wekan_url}{rest_url}"

        headers = dict()

        if kwargs.get("authed", True):
            headers["Authorization"] = f"Bearer {self.token}"

        if method in ("post", "put"):
            headers["Content-type"] = "application/json"

        if rest_url == "/users/login":
            headers["Content-type"] = "application/x-www-form-urlencoded"

        api_response = requests.request(method, request_url,
                                        data=data,
                                        headers=headers,
                                        verify=Wykan.verify_tls)

        if api_response.status_code != 200:
            raise HTTPError(api_response)

        response_json = api_response.json()

        if type(response_json) == dict and response_json.get("error"):
            raise WekanException(str(response_json))

        return api_response.json()

    def get_user_by_username(self, username) -> User:
        """
        Retunn a `User` by a username.
        :param username: Username to search by
        """

        users = self.get_all_users()
        return users.get(username)

    def get_user(self, id) -> User:
        """
        Gets a single user.
        :param id: ID of the user.
        """

        raw_user = self.get(f"/api/users/{id}")
        return User(self, id, raw_user)

    def get_all_users(self):
        all_users = self.get("/api/users")
        return [self.get_user(user_id["_id"]) for user_id in all_users]
