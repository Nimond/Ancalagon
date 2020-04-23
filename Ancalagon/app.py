import json

from .route import Router
from .request import Request


class App:
    def __init__(self, debug=False):
        self.debug = debug
        self.router = Router()

    async def __call__(self, scope, receive, send):
        print(scope)

        path = scope['path']
        method = scope['method']
        request = Request(scope)

        receive = await receive()
        if request.headers.get('content-type') == 'application/json':
            request.json = json.loads(receive['body'])  # TODO: in executor

        response = await self.router.call_route(path, method, request)
        if not response:
            response = '500 Internal Server Error'

        print(f'Respose: {response}')

        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": bytes(response, encoding='utf-8'),
            }
        )

    def route(self, route):
        self.router.add_route(route)
