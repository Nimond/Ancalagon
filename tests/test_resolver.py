from collections import defaultdict
from unittest.mock import AsyncMock, call

import pytest

from ancalagon.resolver import Resolver
from ancalagon.routes import Route
from ancalagon.responses import Response


async def handler(request):
    return Response('<h1>OK</h1>')


@pytest.fixture
def resolver():
    return Resolver()


@pytest.fixture
def route():
    return '/test', handler


def test_resolver_add_route(resolver, route):
    method = 'GET'

    assert resolver.routes == defaultdict(list)

    resolver.add_route(*route)

    assert method in resolver.routes
    assert len(resolver.routes[method]) == 1
