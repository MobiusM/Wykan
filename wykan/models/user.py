from . import _WekanObject


class User(_WekanObject):
    """
    A Wekan user.
    """

    def __init__(self, api, id: str):
        super().__init__(api, id)
        user = self._api.get(f"/api/users/{self.id}")

        self.username = user.get("username")
        self.emails = [UserEmail(email.get("address"), email.get("verified")) for email in user.get("emails")]
        self.created_at = user.get("createdAt")
        self.modified_at = user.get("modifiedAt")
        self.profile = UserProfile(user.get("profile"))
        self.services = user.get("services")
        self.heartbeat = user.get("heartbeat")
        self.is_admin = user.get("isAdmin")
        self.created_though_api = user.get("createdThroughApi")
        self.login_disabled = user.get("loginDisabled")
        self.authentication_method = user.get("authenticationMethod")


class UserEmail:
    """
    A Wekan user's email details
    """

    def __init__(self, address: str, verified: str):
        self.address = address
        self.verified = verified


class UserProfile:
    """
    A Wekan user's profile details.
    """

    def __init__(self, profile: dict):
        self.avatar_url = profile.get("avatarUrl")
        self.email_buffer = profile.get("emailBuffer", [])
        self.fullname = profile.get("fullname")
        self.show_desktop_drag_handles = profile.get("showDesktopDragHandles")
        self.hidden_system_messages = profile.get("hiddenSystemMessages")
        self.hidden_minicard_label_text = profile.get("hiddenMinicardLabelText")
        self.initials = profile.get("initials")
        self.invited_boards = profile.get("invitedBoards", [])
        self.language = profile.get("language")
        self.notifications = profile.get("notifications", [])
        self.show_cards_count_at = profile.get("showCardsCountAT")
        self.starred_boards = profile.get("starredBoards", [])
        self.icode = profile.get("icode")
        self.board_view = profile.get("boardView")
        self.list_sort_by = profile.get("listSortBy")
        self.templates_board_id = profile.get("templatesBoardId")
        self.card_templates_swimlane_id = profile.get("cardTemplatesSwimlaneId")
        self.list_templates_swimlane_id = profile.get("listTemplatesSwimlaneId")
        self.board_templates_swimlane_id = profile.get("boardTemplatesSwimlaneId")
