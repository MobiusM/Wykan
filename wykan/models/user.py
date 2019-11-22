from . import _WekanObject


class User(_WekanObject):
    def __init__(self, id: str):
        super().__init__(id)
