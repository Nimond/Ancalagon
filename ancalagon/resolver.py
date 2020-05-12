from collections import defaultdict
from functools import partial

from .request import Request
from .responses import Response
from .routes import Route


class Resolver:
    def __init__(self):
        self.routes = defaultdict(list)

    async def __call__(self, scope, receive, send):
        scope['request'] = request = Request(scope, receive, send)

        app = scope['app']
        path = scope['path']
        method = scope['method']

        for route in self.routes.get(method, []) + self.routes.get('*', []):
            if route.path == path:
                handler = route.handler
                for middleware in app.middlewares[::-1] + route.middlewares:
                    if middleware not in route.ignore_middlewares:
                        handler = partial(middleware, handler)

                response = await handler(request)

                break
        else:
            response = Response('<h1>404 Not found</h1>', 404)

        await response(scope, receive, send)

    def add_route(self, *args, **kwargs):
        print(args)
        route = Route(*args, **kwargs)

        for method in route.methods:
            self.routes[method].append(route)
