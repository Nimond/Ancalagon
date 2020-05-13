from multidict import CIMultiDict


class Response:
    content_type = b'text/html'

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
        await send({"type": "http.response.body", "body": body})

    def render_body(self):
        return self.body.encode('utf-8')
