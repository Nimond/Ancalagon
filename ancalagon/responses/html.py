from .base import BaseResponse


class HTMLResponse(BaseResponse):
    content_type = b'text/html'

    def render_body(self):
        return self.body.encode('utf-8')
