import re
from unittest.mock import AsyncMock

import pytest

from ancalagon.routes import Route


@pytest.fixture
def path():
    return '/'


@pytest.fixture
def re_path():
    return '/<user_id:int>'


@pytest.fixture
def path_params_cast(re_path):
    return re.findall(r'<(\w+):(\w+)>', re_path)


@pytest.fixture
def handler():
    return AsyncMock()


@pytest.fixture
def methods():
    return ['GET']


@pytest.fixture
def middlewares():
    return [AsyncMock(), AsyncMock()]


@pytest.fixture
def ignore_middlewares():
    return [AsyncMock()]


def test_route(path, handler, methods, middlewares, ignore_middlewares):
    route = Route(path, handler, methods, middlewares, ignore_middlewares)

    assert route.path == path
    assert route.handler == handler
    assert route.methods == methods
    assert route.middlewares == middlewares
    assert route.ignore_middlewares == ignore_middlewares


def test_route_re(
    re_path,
    handler,
    methods,
    middlewares,
    ignore_middlewares,
    path_params_cast,
):
    route = Route(re_path, handler, methods, middlewares, ignore_middlewares)

    assert route.path == re_path
    assert route.handler == handler
    assert route.methods == methods
    assert route.middlewares == middlewares
    assert route.ignore_middlewares == ignore_middlewares

    assert route.path_params_cast == path_params_cast
