
from ..groc_default.groc_base import Groc


class DataLakeFetch(Groc):
    api_endpoint = '/datalake/document/fetch'

    def fetch(self, payload):
        return self.call_api(payload)


class DataLakePush(Groc):
    api_endpoint = '/datalake/document/push'

    def push(self, payload):
        return self.call_api(payload)


class DataLakeCreate(Groc):
    api_endpoint = '/datalake/create'

    def create(self):
        return self.call_api({})


class DataLake:
    def __init__(self):
        self._creator = None
        self._fetcher = None
        self._pusher = None

    def _get_creator(self):
        if self._creator is None:
            self._creator = DataLakeCreate()
        return self._creator

    def _get_fetcher(self):
        if self._fetcher is None:
            self._fetcher = DataLakeFetch()
        return self._fetcher

    def _get_pusher(self):
        if self._pusher is None:
            self._pusher = DataLakePush()
        return self._pusher

    def fetch(self, payload):
        return self._get_fetcher().fetch(payload)

    def push(self, payload):
        return self._get_pusher().push(payload)

    def create(self):
        return self._get_creator().create()
