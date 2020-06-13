import logging

from ancalagon.resolvers import HTTPResolver, WSResolver
from ancalagon.utils import pretty_format, run_func


class App:
    """
    ASGI App
    """

    def __init__(self, debug=False, startup=[], shutdown=[], middlewares=[]):
        self.debug = debug
        self.http = HTTPResolver()
        self.ws = WSResolver()
        self.startup = startup
        self.shutdown = shutdown
        self.middlewares = middlewares

        self.logger = logging.getLogger('simple_example')
        self.logger.setLevel(logging.DEBUG if debug else logging.WARNING)

    async def __call__(self, scope, receive, send):
        self.logger.debug(pretty_format(scope))

        scope['app'] = self

        if scope['type'] == 'lifespan':
            await self.lifespan(receive, send)
        elif scope['type'] == 'http':
            await self.http(scope, receive, send)
        elif scope['type'] == 'websocket':
            await self.ws(scope, receive, send)

    async def lifespan(self, receive, send):
        """
        ASGI lifespan protocol
        """

        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                for func in self.startup:
                    await run_func(func, self)
                await send({'type': 'lifespan.startup.complete'})

            elif message['type'] == 'lifespan.shutdown':
                for func in self.shutdown:
                    await run_func(func, self)
                await send({'type': 'lifespan.shutdown.complete'})
                return

    def route(self, *args, **kwargs):
        """
        HTTPResolver.add_route  shortcut
        """

        self.http.add_route(*args, **kwargs)

    def websocket_route(self, *args, **kwargs):
        """
        WSResolver.add_route  shortcut
        """

        self.ws.add_route(*args, **kwargs)
