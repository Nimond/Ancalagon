from unittest.mock import AsyncMock

import pytest
from multidict import CIMultiDict, MultiDict

from ancalagon.request import Request
from ancalagon.url import URL


@pytest.fixture
def scope():
    return {
        'scheme': 'http',
        'server': ('localhost', 5000),
        'path': '/test',
        'client': 'localhost:5001',
        'query_string': b'a=1&b=2',
        'http_version': '1.1',
        'app': 'app_mock',
        'path_params': {},
        'headers': [(b'HeAdErNaMe', b'value')],
        'method': 'GET',
    }


@pytest.fixture
def req(scope):  # request is a reserver pytest fixture name
    return Request(scope, AsyncMock(), AsyncMock())


def test_request_create(req, scope):
    assert req._scope == scope


@pytest.mark.asyncio
async def test_properties(req, scope):
    for key, value in scope.items():
        if key not in ('headers', 'request'):
            print(key)
            assert getattr(req, key) == value

    assert req.url.string == URL(scope).string

    assert req.query == MultiDict(a='1', b='2')
    assert hasattr(req, '_query')

    assert req.headers == CIMultiDict(HEADERNAME='value')
    assert hasattr(req, '_headers')

    req._receive.return_value = {'body': b'{"a": 1}'}
    assert await req.json() == {'a': 1}
    assert hasattr(req, '_json')
    req._receive.assert_awaited_once_with()
