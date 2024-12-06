
from ..groc_default.groc_base import Groc


class VectorLakeFetch(Groc):
    api_endpoint = '/vector/fetch'

    def fetch(self, query):
        return self.call_api({'query': query})


class VectorLakePush(Groc):
    api_endpoint = '/vector/push'

    def push(self, payload):
        return self.call_api(payload)


class VectorLakeSearch(Groc):
    api_endpoint = '/vector/search'

    def search(self, payload):
        return self.call_api(payload)


class VectorLakeCreate(Groc):
    api_endpoint = '/vector/create'

    def create(self):
        return self.call_api({})


class VectorLake:
    def __init__(self):
        self._fetcher = None
        self._pusher = None
        self._searcher = None
        self._creator = None

    def _get_fetcher(self):
        if self._fetcher is None:
            self._fetcher = VectorLakeFetch()
        return self._fetcher

    def _get_pusher(self):
        if self._pusher is None:
            self._pusher = VectorLakePush()
        return self._pusher

    def _get_searcher(self):
        if self._searcher is None:
            self._searcher = VectorLakeSearch()
        return self._searcher

    def _get_creator(self):
        if self._creator is None:
            self._creator = VectorLakeCreate()
        return self._creator

    def fetch(self, query):
        return self._get_fetcher().fetch(query)

    def push(self, payload):
        return self._get_pusher().push(payload)

    def search(self, payload):
        return self._get_searcher().search(payload)

    def create(self):
        return self._get_creator().create()
