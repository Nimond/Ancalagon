import asyncio

from multidict import CIMultiDict


class StreamResponse:
    content_type = b'application/octet-stream'

    def __init__(self, request, status_code=200):
        self._scope = request._scope
        self._receive = request._receive
        self._send = request._send
        self.prepared = False
        self.disconnected = False

        self.status_code = status_code
        self.headers = CIMultiDict()

    async def is_disconnected(self):
        if self.disconnected:
            return True

        while True:
            message = await self._receive()
            if message["type"] == "http.disconnect":
                self.disconnected = True
                return True

    async def prepare(self):
        self.prepared = True
        await self._send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    [b'content-type', self.content_type],
                    [b'server', b'Ancalagon'],
                ]
                + [
                    [key.encode('utf-8'), value.encode('utf-8')]
                    for key, value in self.headers.items()
                ],
            }
        )

    async def write(self, body):
        if self.disconnected:
            return False

        if not self.prepared:
            await self.prepare()

        send = self._send(
            {
                "type": "http.response.body",
                "body": body.encode('utf-8'),
                'more_body': True,
            }
        )
        await asyncio.wait(
            (send, self.is_disconnected()),
            return_when=asyncio.FIRST_COMPLETED,
        )

    async def __call__(self, scope, receive, send):
        if not self.disconnected:
            await send({"type": "http.response.body", "body": b''})
