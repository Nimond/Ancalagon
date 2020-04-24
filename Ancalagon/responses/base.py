class Response:
    content_type = b'text/html'

    def __init__(self, body='', status_code=200):
        self.body = body
        self.status_code = status_code

    async def __call__(self, scope, receive, send):
        body = self.render_body()
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [[b"content-type", self.content_type]],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": body,
            }
        )

    def render_body(self):
        return self.body.encode('utf-8')
