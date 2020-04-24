import json


class Request:
    def __init__(self, scope, receive, send):
        scope['request'] = self

        self._scope = scope
        self._receive = receive
        self._send = send
        self.headers = self._parse_headers(scope['headers'])

    def _parse_headers(self, raw_headers):
        return {h[0].decode(): h[1].decode() for h in raw_headers}

    async def body(self):
        chunks = []
        while True:
            receive = await self._receive()
            chunks.append(receive['body'])
            if not receive.get('more_body'):
                break

        return b''.join(chunks)

    async def json(self):
        return json.loads(await self.body())  # TODO: in executor

    @property
    def path_params(self):
        return self._scope.get('path_params', {})
