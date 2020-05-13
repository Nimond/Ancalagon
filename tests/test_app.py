from unittest.mock import AsyncMock, Mock

import pytest

from ancalagon import App


@pytest.fixture
def scope():
    return {'type': 'http'}


@pytest.fixture
def startup():
    return [AsyncMock()]


@pytest.fixture
def shutdown():
    return [AsyncMock()]


@pytest.fixture
def middlewares():
    return []


@pytest.fixture
def add_route():
    return Mock()


@pytest.fixture
async def resolver_callable(add_route):
    resolver_callable = AsyncMock()
    resolver_callable.add_route = add_route

    return resolver_callable


@pytest.fixture
def app(startup, shutdown, middlewares, resolver_callable):
    app = App(
        debug=True,
        startup=startup,
        shutdown=shutdown,
        middlewares=middlewares,
    )
    app.http = resolver_callable

    return app


def test_create(app, startup, shutdown, middlewares):
    assert app.debug is True
    assert app.startup is startup
    assert app.shutdown is shutdown
    assert app.middlewares is middlewares


def test_route(app):
    args = ('/', Mock())
    app.route(args)

    app.http.add_route.assert_called_once_with(args)


@pytest.mark.asyncio
async def test_call_http(app, scope):
    receive = AsyncMock()
    send = AsyncMock()

    await app(scope, receive, send)

    app.http.assert_awaited_once_with(scope, receive, send)


@pytest.mark.asyncio
async def test_call_lifespan(app, scope):
    scope['type'] = 'lifespan'

    receive = AsyncMock(
        side_effect=(
            {'type': 'lifespan.startup'},
            {'type': 'lifespan.shutdown'},
        ),
    )
    send = AsyncMock()

    await app(scope, receive, send)

    for mock in app.startup + app.shutdown:
        mock.assert_awaited_once_with(app)
