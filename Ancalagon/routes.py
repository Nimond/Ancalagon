import re


class Route:
    def __init__(self, path, handler, methods):
        self.path = path
        self.methods = methods
        self.handler = handler

        groups = re.findall(r'<(\w+):(\w+)>', self.path)
        if groups:
            self.path_params_cast = groups
