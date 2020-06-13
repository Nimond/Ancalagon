from functools import partial

from ancalagon.requests import WSRequest
from ancalagon.responses import Response
from ancalagon.routes import WSRoute


class WSResolver:
    def __init__(self):
        self.routes = []

    async def __call__(self, scope, receive, send):
        path = scope['path']
        websocket = (scope, receive, send)

        r = await receive()
        print(r)
        assert r['type'] == 'websocket.connect'

        # while True:
        #     print(await receive())

        for route in self.routes:
            if route.path == path:
                await send({'type': 'websocket.accept'})
                await route.handler(websocket)
                break

        await send({'type': 'websocket.close'})

    def add_route(self, *args, **kwargs):
        route = WSRoute(*args, **kwargs)
        self.routes.append(route)
