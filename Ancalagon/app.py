from .resolver import Resolver
from .routes import Route


class App:
    def __init__(self, debug=False):
        self.debug = debug
        self.resolver = Resolver()

    async def __call__(self, scope, receive, send):
        await self.resolver(scope, receive, send)

    def route(self, path, handler, methods=['GET']):
        self.resolver.add_route(Route(path, handler, methods))
