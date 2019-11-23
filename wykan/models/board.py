from . import _WekanObject
from .colors import Colors, BoardColors


class Board(_WekanObject):
    """
    Wekan Board object
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

        self.members = [self._api.get_user(member.get("userId")) for member in board.get("members")]
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


class BoardLabel:

    def __init__(self, id: str, name: str, color: BoardColors):
        self.id = id
        self.name = name
        self.color = color
