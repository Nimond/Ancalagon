from multidict import CIMultiDict


class BaseResponse:
    content_type = None

    def __init__(self, body='', status_code=200):
        self.body = body
        self.status_code = status_code
        self.headers = CIMultiDict()

    async def __call__(self, scope, receive, send):
        body = self.render_body()
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.build_headers(),
            }
        )
        await send({"type": "http.response.body", "body": body})

    def build_headers(self):
        return [
            [b'content-type', self.content_type],
            [b'server', b'Ancalagon'],
        ]
        + [
            [key.encode('utf-8'), value.encode('utf-8')]
            for key, value in self.headers.items()
        ]

    def render_body(self):
        raise NotImplementedError
