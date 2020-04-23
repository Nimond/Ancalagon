class Request:
    def __init__(self, scope):
        self.headers = self.parse_headers(scope['headers'])

    def parse_headers(self, raw_headers):
        return {h[0].decode(): h[1].decode() for h in raw_headers}
