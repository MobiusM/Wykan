from wykan.models.list import List
from . import _WekanObject
from .colors import Colors, BoardColors


class Board(_WekanObject):
    """
    A Wekan board.
    """

    def __init__(self, api, id: str):
        super().__init__(api, id)
        board = self._api.get(f"/api/boards/{self.id}")

        self.title = board.get("title")
        self.slug = board.get("slug")
        self.archived = board.get("archived")
        self.created_at = board.get("createdAt")
        self.modified_at = board.get("modifiedAt")
        self.stars = board.get("stars")

        self.labels = list()
        for label in board.get("labels"):
            self.labels.append(BoardLabel(label.get("_id"), label.get("name"), Colors[label.get("color")]))

        self.members = list()
        for member in board.get("members"):
            self.members.append(BoardMember(
                self._api.get_user(member.get("userId")),
                member.get("isAdmin"),
                member.get("isNoComments"),
                member.get("isCommentOnly")
            ))

        self.permission = board.get("permission")
        self.color = BoardColors[board.get("color")]
        self.description = board.get("description")
        self.subtasks_default_board_id = board.get("subtasksDefaultBoardId")
        self.subtasks_default_list_id = board.get("subtasksDefaultListId")
        self.allows_subtasks = board.get("allowsSubtasks")
        self.present_parent_task = board.get("presentParentTask")
        self.start_at = board.get("startAt")
        self.due_at = board.get("dueAt")
        self.end_at = board.get("endAt")
        self.spent_time = board.get("spentTime")
        self.is_overtime = board.get("isOvertime")
        self.type = board.get("type")

    def change_member_permissions(self, user_id, is_board_admin: bool, is_no_comments: bool, is_comment_only: bool):
        """
        Change the permission of a member of the board.
        :param user_id: ID of the user to change.
        :param is_board_admin: Can view and edit cards, remove members, and change settings for the board.
        :param is_no_comments: Can not see comments and activities.
        :param is_comment_only: Can comment on cards only.
        """

        change_user_details = {
            "isAdmin": is_board_admin,
            "isNoComments": is_no_comments,
            "isCommentOnly": is_comment_only
        }
        self._api.post(f"/api/boards/{self.id}/members/{user_id}", change_user_details)

    def add_board_member(self, user_id, is_board_admin: bool, is_no_comments: bool, is_comment_only: bool):
        """
        Add a user to the board.
        :param user_id: ID of the user to add.
        :param is_board_admin: Can view and edit cards, remove members, and change settings for the board.
        :param is_no_comments: Can not see comments and activities.
        :param is_comment_only: Can comment on cards only.
        """

        add_user_details = {
            "action": "add",
            "isAdmin": is_board_admin,
            "isNoComments": is_no_comments,
            "isCommentOnly": is_comment_only
        }
        self._api.post(f"/api/boards/{self.id}/members/{user_id}/add", add_user_details)

    def get_lists(self) -> [List]:
        """
        Get all the lists in this board.
        """

        board_lists = self._api.get(f"/api/boards/{self.id}/lists")
        return [self.get_list(board_list.get("_id")) for board_list in board_lists]

    def get_list(self, list_id) -> List:
        """
        Get a single list.
        :param list_id: ID of the list.
        """

        return List(self._api, self.id, list_id)

    def create_list(self, title: str) -> List:
        """
        Add a list to the board.
        :param title: Title of the list to add.
        """

        new_list_details = {
            "title": title
        }

        new_list = self._api.post(f"/api/boards/{self.id}/lists", new_list_details)
        return List(self._api, self.id, new_list["_id"])

    def delete_list(self, list_id) -> str:
        """
        Delete a list from the board.
        :param list_id: ID of the list to delete.
        :return ID of the delete list.
        """

        return self._api.delete(f"/api/boards/{self.id}/lists/{list_id}")


class BoardLabel:
    """
    A board label.
    """

    def __init__(self, id: str, name: str, color: BoardColors):
        self.id = id
        self.name = name
        self.color = color


class BoardMember:
    """
    A board member.
    """

    def __init__(self, user, is_board_admin: bool, is_no_comments: bool, is_comment_only: bool):
        """
        :param user: A Wekan user.
        :param is_board_admin: Can view and edit cards, remove members, and change settings for the board.
        :param is_no_comments: Can not see comments and activities.
        :param is_comment_only: Can comment on cards only.
        """

        self.user = user
        self.is_board_admin = is_board_admin
        self.is_no_comment = is_no_comments
        self.is_comment_only = is_comment_only
