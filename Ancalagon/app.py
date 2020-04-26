from .resolver import Resolver
from .routes import Route
from .utils import run_func, prettyformat


class App:
    def __init__(self, debug=False, startup=[], shutdown=[]):
        self.debug = debug
        self.http = Resolver()
        self.startup = startup
        self.shutdown = shutdown

    async def __call__(self, scope, receive, send):
        print(prettyformat(scope))

        # TODO: middlewares
        scope['app'] = self

        if scope['type'] == 'lifespan':
            await self.lifespan(scope, receive, send)
        elif scope['type'] == 'http':
            await self.http(scope, receive, send)

    async def lifespan(self, scope, receive, send):
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                print('Dragon: lifespan:start')
                for func in self.startup:
                    await run_func(func, scope['app'])
                await send({'type': 'lifespan.startup.complete'})

            elif message['type'] == 'lifespan.shutdown':
                print('Dragon: lifespan:shutdown')
                for func in self.shutdown:
                    await run_func(func)
                await send({'type': 'lifespan.shutdown.complete'})
                return

    def route(self, path, handler, methods=['GET']):
        self.http.add_route(Route(path, handler, methods))
