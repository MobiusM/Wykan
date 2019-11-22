from . import _WekanObject


class Card(_WekanObject):
    """
    Wekan Card
    """

    def __init__(self, id: str):
        super().__init__(id)
