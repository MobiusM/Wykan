from . import _WekanObject, Colors


class BoardLabel(_WekanObject):

    def __init__(self, id: str, name: str, color: Colors):
        super().__init__(id)
        self.name = name
        self.color = color
