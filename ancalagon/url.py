class URL:
    def __init__(self, _scope):
        self.scheme = _scope['scheme']
        self.host = _scope['server'][0]
        self.port = _scope['server'][1]
        self.path = _scope['path']

    def __str__(self):
        return f'{self.scheme}://{self.host}:{self.port}{self.path}'

    def __repr__(self):
        return f'{self.scheme}://{self.host}:{self.port}{self.path}'
