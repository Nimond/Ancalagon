import json


class Request:
    def __init__(self, scope, receive, send):
        scope['request'] = self

        self._scope = scope
        self._receive = receive
        self._send = send

        self.method = scope['method']

    async def body(self):
        chunks = []
        while True:
            receive = await self._receive()
            chunks.append(receive['body'])
            if not receive.get('more_body'):
                break

        return b''.join(chunks)

    @property
    def headers(self):
        if hasattr(self, '_headers'):
            return self._headers
        else:
            self._headers = {
                h[0].decode(): h[1].decode() for h in self._scope['headers']
            }
            return self._headers

    async def json(self):
        if hasattr(self, '_json'):
            return self._json
        else:
            self._json = json.loads(await self.body())  # TODO: in executor
            return self._json

    @property
    def path_params(self):
        return self._scope.get('path_params', {})

    @property
    def query(self):
        # TODO: MultiDict
        query_string = self._scope.get('query_string').decode()
        return {
            q.split('=')[0]: q.split('=')[1] for q in query_string.split('&')
        }
