from unittest.mock import AsyncMock, Mock, call

import pytest

from ancalagon.responses import StreamResponse


@pytest.fixture
def status_code():
    return 201


@pytest.fixture
def req():
    req = Mock()
    req._scope = {}
    req._receive = AsyncMock(return_value={"type": "http.disconnect"})
    req._send = AsyncMock()

    return req


@pytest.fixture
def response(status_code, req):
    return StreamResponse(req, status_code)


def test_response(response, status_code, req):
    assert response._scope == req._scope
    assert response._receive == req._receive
    assert response._send == req._send
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_send_response(response, req):
    body = b'body'

    calls = [
        call(
            {
                "type": "http.response.start",
                "status": response.status_code,
                "headers": [
                    [b"content-type", response.content_type],
                    [b'server', b'Ancalagon'],
                ],
            }
        ),
        call({"type": "http.response.body", "body": body, 'more_body': True}),
    ]

    await response.write(body.decode('utf-8'))

    assert req._send.await_count == 2
    req._send.assert_has_awaits(calls)

    assert await response.is_disconnected() is True

    assert await response.write(body) is False

    response.disconnected = False

    await response(req._scope, req._receive, req._send)

    assert req._send.await_count == 3
    req._send.assert_awaited_with({"type": "http.response.body", "body": b''})
