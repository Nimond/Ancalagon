import json

from .base import BaseResponse


class JSONResponse(BaseResponse):
    content_type = b'application/json'

    def render_body(self):
        return json.dumps(
            self.body,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
        ).encode('utf-8')
