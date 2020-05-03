import json
from multidict import CIMultiDict, MultiDict

from .url import URL


class Request:
    def __init__(self, scope, receive, send):
        scope['request'] = self
        self._scope = scope
        self._receive = receive
        self._send = send
        self._url = URL(scope)

    async def body(self):
        if hasattr(self, '_body'):
            return self._body
        else:
            chunks = []
            while True:
                receive = await self._receive()
                chunks.append(receive['body'])
                if not receive.get('more_body'):
                    break

            self._body = b''.join(chunks)
            return self._body

    async def json(self):
        if hasattr(self, '_json'):
            return self._json
        else:
            self._json = json.loads(await self.body())  # TODO: in executor
            return self._json

    @property
    def headers(self):
        if hasattr(self, '_headers'):
            return self._headers
        else:
            self._headers = CIMultiDict(
                {h[0].decode(): h[1].decode() for h in self._scope['headers']}
            )
            return self._headers

    @property
    def query(self):
        if hasattr(self, '_query'):
            return self._query
        else:
            query_string = self._scope.get('query_string').decode()
            self._query = MultiDict(
                {
                    q.split('=')[0]: q.split('=')[1]
                    for q in query_string.split('&')
                }
            )
            return self._query

    @property
    def path_params(self):
        return self._scope.get('path_params', {})

    @property
    def method(self):
        return self._scope['method']

    @property
    def app(self):
        return self._scope['app']

    @property
    def path(self):
        return self._scope['path']

    @property
    def http_version(self):
        return self._scope['http_version']

    @property
    def query_string(self):
        return self._scope['query_string']

    @property
    def url(self):
        return self._url

    @property
    def client(self):
        return self._scope.get('client')
