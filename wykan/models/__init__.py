from .board import Board


class _WekanObject:
    """
        Base Wekan object
        _id: id of object
    """

    def __init__(self, id: str):
        self._id = id

    @property
    def id(self) -> str:
        return self._id
