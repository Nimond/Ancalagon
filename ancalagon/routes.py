import re
from typing import Awaitable, List

from ancalagon.responses import Response


class Route:
    def __init__(
        self,
        path: str,
        handler: Awaitable[Response],
        methods: List[str] = None,
        middlewares: List[Awaitable[Response]] = None,
        ignore_middlewares: List[Awaitable[Response]] = None,
    ) -> None:
        self.path = path
        self.methods = methods
        self.handler = handler
        self.middlewares = middlewares
        self.ignore_middlewares = ignore_middlewares

        groups = re.findall(r'<(\w+):(\w+)>', self.path)
        if groups:
            self.path_params_cast = groups
