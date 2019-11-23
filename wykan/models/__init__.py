class _WekanObject:
    """
        Base Wekan object
        _id: id of object
    """

    def __init__(self, api, id: str, raw_object):
        self._api = api
        self._id = id
        self._raw_object = raw_object

    @property
    def id(self) -> str:
        return self._id
