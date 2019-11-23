from . import _WekanObject
from collections import namedtuple

user_email = namedtuple("user_email", "address verified")


class User(_WekanObject):
    def __init__(self, api, id: str, raw_user: dict, **kwargs):
        super().__init__(api, id, raw_user)

        self.username = raw_user.get("username")
        self.emails = UserEmail(kwargs.get("address"), kwargs.get("verified"))
        self.created_at = raw_user.get("createdAt")
        self.modified_at = raw_user.get("modifiedAt")
        # self.profile = UserProfile(raw_user)  # todo: is this the right appoach?
        self.services = raw_user.get("services")
        self.heartbeat = raw_user.get("heartbeat")
        self.is_admin = raw_user.get("isAdmin")
        self.created_though_api = raw_user.get("createdThroughApi")
        self.login_disabled = raw_user.get("loginDisabled")
        self.authentication_method = raw_user.get("authenticationMethod")

    def populate_user_data(self):
        pass


class UserEmail:

    def __init__(self, address: str, verified: str):
        self.address = address
        self.verified = verified


class UserProfile:

    def __init__(self, ):
        pass
