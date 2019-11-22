import requests

from .models import Board


class Wykan:

    def __init__(self, api_url, credentials, proxies=None):
        if proxies is None:
            proxies = {}
        self.session = requests.Session()
        self.proxies = proxies
        self.api_url = api_url
        api_login = self.api_call("/users/login", method="post", data=credentials, authed=False)
        self.token = api_login["token"]
        self.user_id = api_login["id"]

    def api_call(self, rest_url, method, data=None, authed=True):
        request_url = f"{self.api_url}{rest_url}"

        api_response = requests.request(method, request_url,
                                        data=data,
                                        headers={"Authorization": "Bearer {}".format(self.token)} if authed else {},
                                        proxies=self.proxies)

        return api_response.json()

    def get_user_boards(self):
        boards_data = self.api_call("/api/users/{}/boards".format(self.user_id), method="get")
        return [Board(self, board_data) for board_data in boards_data]
