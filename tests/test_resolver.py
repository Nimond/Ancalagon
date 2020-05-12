from collections import defaultdict
from unittest.mock import AsyncMock, Mock

import pytest

from ancalagon.resolver import Resolver


async def middleware_one(handler, request):
    request.mark_one = 'here was middleware_one'

    return await handler(request)


async def middleware_two(handler, request):
    request.mark_two = 'here was middleware_two'

    return await handler(request)


@pytest.fixture
def app():
    app = Mock()
    app.middlewares = []

    return app


@pytest.fixture
def path():
    return '/test'


@pytest.fixture
def scope(path, app):
    return {
        'scheme': 'http',
        'server': ('localhost', 5000),
        'app': app,
        'method': 'GET',
        'path': path
    }


@pytest.fixture
def resolver():
    return Resolver()


def test_resolver_add_route(resolver, path):
    method = 'GET'

    assert resolver.routes == defaultdict(list)

    resolver.add_route(path, AsyncMock())

    assert method in resolver.routes
    assert len(resolver.routes[method]) == 1


@pytest.mark.asyncio
async def test_resolver_call_not_found(resolver, path, scope, monkeypatch):
    handler = AsyncMock()
    resolver.add_route(path, handler)

    scope['path'] = '/we_have_no_such_path'

    receive = AsyncMock()
    send = AsyncMock()

    response_callable = AsyncMock()
    response = Mock(return_value=response_callable)
    monkeypatch.setattr('ancalagon.resolver.Response', response)

    await resolver(scope, receive, send)

    response.assert_called_once_with('<h1>404 Not found</h1>', 404)
    response_callable.assert_awaited_once_with(scope, receive, send)
    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_resolver_call_without_middlewares(resolver, path, scope):
    response_callable = AsyncMock()
    handler = AsyncMock(return_value=response_callable)
    resolver.add_route(path, handler)

    receive = AsyncMock()
    send = AsyncMock()

    await resolver(scope, receive, send)

    handler.assert_awaited()
    response_callable.assert_awaited_once_with(scope, receive, send)


@pytest.mark.asyncio
async def test_middlewares(resolver, path, scope):
    scope['app'].middlewares.append(middleware_one)
    scope['app'].middlewares.append(middleware_two)

    response_callable = AsyncMock()
    handler = AsyncMock(return_value=response_callable)
    resolver.add_route(path, handler, ignore_middlewares=[middleware_two])

    receive = AsyncMock()
    send = AsyncMock()

    await resolver(scope, receive, send)

    handler.assert_awaited()
    response_callable.assert_awaited_once_with(scope, receive, send)

    request = handler.call_args_list[0].args[0]

    assert request.mark_one == 'here was middleware_one'
    assert not hasattr(request, 'mark_two')
