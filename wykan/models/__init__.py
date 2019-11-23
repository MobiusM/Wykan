class _WekanObject:
    """
        Base Wekan object
        _id: id of object
    """

    def __init__(self, api, id: str):
        self._api = api
        self._id = id

    @property
    def id(self) -> str:
        return self._id
