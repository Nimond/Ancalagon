class URL:
    def __init__(self, _scope):
        self.sheme = _scope['sheme']
        self.host = _scope['server'][0]
        self.port = _scope['server'][1]
        self.path = _scope['path']

    def __str__(self):
        return f'{self.sheme}://{self.host}:{self.port}{self.path}'

    def __repr__(self):
        return f'{self.sheme}://{self.host}:{self.port}{self.path}'
