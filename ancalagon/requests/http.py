import json

from .base import BaseRequest


class HTTPRequest(BaseRequest):
    async def body(self):
        if not hasattr(self, '_body'):
            chunks = []
            while True:
                response = await self._receive()
                chunks.append(response['body'])
                if not response.get('more_body'):
                    break

            self._body = b''.join(chunks)

        return self._body

    async def json(self):
        if not hasattr(self, '_json'):
            self._json = json.loads(await self.body())

        return self._json

    @property
    def method(self):
        return self._scope['method']
