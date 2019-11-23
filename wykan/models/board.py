from . import _WekanObject


class Board(_WekanObject):
    """
    Wekan Board object
    """

    def __init__(self, a, board_data):
        super().__init__(api, board_data)
        self.title = self.data["title"]

    def cardslists(self):
        cardslists_data = self.api.api_call("/api/boards/{}/lists".format(self.id), method="get")
        return [Cardslist(self.api, self, cardslist_data) for cardslist_data in cardslists_data]

    def swimlanes(self):
        swimlanes_data = self.api.api_call(f"/api/boards/{self.id}/swimlanes", method="get")
        return [SwimLane(self.api, self, swimlane_data) for swimlane_data in swimlanes_data]

    def pprint(self, indent=0):
        pprint = "{}- {}".format("  " * indent, self.title)
        for cardslist in self.cardslists():
            pprint += "\n{}".format(cardslist.pprint(indent + 1))
        return pprint
