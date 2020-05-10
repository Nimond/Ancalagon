import logging

from .resolver import Resolver
from .utils import pretty_format, run_func


class App:
    """
    ASGI App
    """

    def __init__(self, debug=False, startup=[], shutdown=[], middlewares=[]):
        self.debug = debug
        self.http = Resolver()
        self.startup = startup
        self.shutdown = shutdown
        self.middlewares = middlewares

        self.logger = logging.getLogger('simple_example')
        self.logger.setLevel(logging.DEBUG if debug else logging.WARNING)

    async def __call__(self, scope, receive, send):
        self.logger.debug(pretty_format(scope))

        # TODO: ASGI middlewares
        scope['app'] = self

        if scope['type'] == 'lifespan':
            await self.lifespan(receive, send)
        elif scope['type'] == 'http':
            await self.http(scope, receive, send)

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
        Resolver.add_route  shortcut
        """

        self.http.add_route(*args, **kwargs)
