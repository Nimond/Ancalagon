import pytest

from ancalagon.url import URL


@pytest.fixture
def scheme():
    return 'http'


@pytest.fixture
def host():
    return 'localhost'


@pytest.fixture
def port():
    return 5000


@pytest.fixture
def server(host, port):
    return host, port


@pytest.fixture
def path():
    return '/'


@pytest.fixture
def scope(scheme, server, path):
    return {
        'scheme': scheme,
        'server': server,
        'path': path,
    }


@pytest.fixture
def full_url(scheme, host, port, path):
    return f'{scheme}://{host}:{port}{path}'


def test_url(scope, full_url):
    url = URL(scope)

    assert url.__str__() == full_url
    assert url.__repr__() == full_url
