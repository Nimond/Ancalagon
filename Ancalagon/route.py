class Route:
    def __init__(self, path, handler, methods=['GET']):
        self.path = path
        self.methods = methods
        self.handler = handler


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    async def call_route(self, path, method, request):
        for route in self.routes:
            if method in route.methods:
                if route.path == path:
                    return await route.handler(request)
        else:
            pass
