import re


class Route:
    def __init__(
        self,
        path,
        handler,
        methods=['GET'],
        middlewares=[],
        ignore_middlewares=[],
    ):
        self.path = path
        self.methods = methods
        self.handler = handler
        self.middlewares = middlewares
        self.ignore_middlewares = ignore_middlewares

        groups = re.findall(r'<(\w+):(\w+)>', self.path)
        if groups:
            self.path_params_cast = groups
