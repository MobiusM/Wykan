import datetime


class _WekanObject:
    """
    Base Wekan object
    _id: id of object
    """

    @property
    def id(self) -> str:
        return self._id

    def __init__(self, api, data: any):
        self._id = data["_id"]
        self.api = api
        self.data = data


class Board(_WekanObject):
    """
    Wekan Board object
    """

    def __init__(self, api, board_data):
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


class SwimLane(_WekanObject):
    def __init__(self, api, board, swimlane_data):
        super().__init__(api, swimlane_data)
        self.board = board
        self.title = self.data["title"]

    def get_cards(self):
        cards_data = self.api.api_call("/api/boards/{}/swimlanes/{}/cards".format(self.board.id, self.id), method="get")
        return [Card(self.api, self, card_data) for card_data in cards_data]

    def pprint(self, indent=0):
        pprint = "{}- {}".format("  " * indent, self.title)
        for cards in self.get_cards():
            pprint += "\n{}".format(cards.pprint(indent + 1))
        return pprint


class Cardslist(_WekanObject):
    """
    Wekan Card List Object
    """

    def __init__(self, api, board, cardslist_data):
        super().__init__(api, cardslist_data)
        self.board = board
        self.title = self.data["title"]

    def get_cards(self):
        cards_data = self.api.api_call("/api/boards/{}/lists/{}/cards".format(self.board.id, self.id), method="get")
        return [Card(self.api, self, card_data) for card_data in cards_data]

    def pprint(self, indent=0):
        pprint = "{}- {}".format("  " * indent, self.title)
        for cards in self.get_cards():
            pprint += "\n{}".format(cards.pprint(indent + 1))
        return pprint


class Card(_WekanObject):
    """
    Wekan Card Object
    """

    def __init__(self, api, cardslist, card_data):
        super().__init__(api, card_data)
        self.cardslist = cardslist
        self.title = self.data["title"]

    def get_card_info(self):
        info_data = self.api.api_call("/api/boards/{}/lists/{}/cards/{}".format(
            self.cardslist.board.id,
            self.cardslist.id,
            self.id), method="get")
        return info_data

    def get_checklists(self):
        checklists_data = self.api.api_call("/api/boards/{}/cards/{}/checklists".format(
            self.cardslist.board.id,
            self.id), method="get")
        return [Checklist(self.api, self, checklist_data) for checklist_data in checklists_data]

    def pprint(self, indent=0):
        pprint = "{}- {}".format("  " * indent, self.title)
        cardinfo = self.get_card_info()
        if "dueAt" in cardinfo:
            pdate = datetime.datetime.strptime(cardinfo["dueAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
            pprint += "\n{}- Due at: {}".format("  " * (indent + 1), pdate)
        for checklist in self.get_checklists():
            pprint += "\n{}".format(checklist.pprint(indent + 1))
        return pprint


class Checklist(_WekanObject):
    """
    Wekan Card List Object
    """

    def __init__(self, api, card, checklist_data):
        super().__init__(api, checklist_data)
        self.card = card
        self.title = self.data["title"]

    def get_items(self):
        items_data = self.api.api_call("/api/boards/{}/cards/{}/checklists/{}".format(
            self.card.cardslist.board.id,
            self.card.id,
            self.id), method="get")
        return [ChecklistItem(self.api, self, item_data) for item_data in items_data["items"]]

    def pprint(self, indent=0):
        pprint = "{}- {}".format("  " * indent, self.title)
        for item in self.get_items():
            pprint += "\n{}".format(item.pprint(indent + 1))
        return pprint


class ChecklistItem(_WekanObject):
    """
    Wekan CheckList Item Object
    """

    def __init__(self, api, checklist, item_data):
        super().__init__(api, item_data)
        self.checklist = checklist
        self.is_finished = self.data["isFinished"]
        self.title = self.data["title"]

    def pprint(self, indent=0):
        pprint = "{}- [{}] {}".format("  " * indent, "X" if self.is_finished else " ", self.title)
        return pprint
