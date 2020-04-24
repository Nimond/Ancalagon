from collections import defaultdict
from .responses import Response
from .request import Request


class Resolver:
    def __init__(self):
        self.routes = defaultdict(list)

    async def __call__(self, scope, receive, send):
        scope['request'] = request = Request(scope, receive, send)
        path = scope['path']
        method = scope['method']

        for route in self.routes.get(method, []) + self.routes.get('*', []):
            if route.path == path:
                response = await route.handler(request)
                break
        else:
            response = Response('<h1>404 Not found</h1>', 404)

        await response(scope, receive, send)

    def add_route(self, route):
        for method in route.methods:
            self.routes[method].append(route)
