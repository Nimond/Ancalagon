import ancalagon.mypy_types as types


class URL:
    def __init__(self, _scope: types.Scope) -> None:
        self.scheme = _scope['scheme']
        self.host = _scope['server'][0]
        self.port = _scope['server'][1]
        self.path = _scope['path']
        self.string = f'{self.scheme}://{self.host}:{self.port}{self.path}'

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return self.string
