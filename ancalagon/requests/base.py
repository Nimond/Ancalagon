from multidict import CIMultiDict, MultiDict

from ancalagon.url import URL


class BaseRequest:
    def __init__(self, scope, receive, send):
        scope['request'] = self
        self._scope = scope
        self._receive = receive
        self._send = send
        self._url = URL(scope)

    @property
    def headers(self):
        if not hasattr(self, '_headers'):
            self._headers = CIMultiDict(
                {h[0].decode(): h[1].decode() for h in self._scope['headers']}
            )

        return self._headers

    @property
    def query(self):
        if not hasattr(self, '_query'):
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

    @property
    def scheme(self):
        return self._scope.get('scheme')

    @property
    def server(self):
        return self._scope.get('server')
