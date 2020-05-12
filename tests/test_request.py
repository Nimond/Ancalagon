from unittest.mock import AsyncMock

import pytest

from ancalagon.request import Request


@pytest.fixture
def scope():
    return {
        'scheme': 'http',
        'server': ('localhost', 5000),
        'path': '/test',
    }


@pytest.fixture
def req(scope):  # request is a reserver pytest fixture name
    return Request(scope, AsyncMock(), AsyncMock())


def test_request_create(req, scope):
    assert req._scope == scope
