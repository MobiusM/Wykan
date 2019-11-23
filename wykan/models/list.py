from . import _WekanObject
from .colors import Colors


class List(_WekanObject):
    """
    Wekan List
    """

    def __init__(self, api, board_id, list_id: str):
        super().__init__(api, list_id)
        _list = self._api.get(f"/api/boards/{board_id}/lists/{list_id}")

        self.title = _list.get("title")
        self.starred = _list.get("starred")
        self.archived = _list.get("archived")
        self.boardId = board_id
        self.swimlaneId = _list.get("swimlaneId")
        self.createdAt = _list.get("createdAt")
        self.sort = _list.get("sort")
        self.updatedAt = _list.get("updatedAt")
        self.modifiedAt = _list.get("modifiedAt")
        self.wipLimit = _list.get("wipLimit")
        self.color = Colors[_list.get("color")] if _list.get("color") else None
        self.type = _list.get("type")
