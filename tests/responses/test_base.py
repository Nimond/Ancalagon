from unittest.mock import AsyncMock, call

import pytest

from ancalagon.responses import Response


@pytest.fixture
def body():
    return '<h1>Updated</h1>'


@pytest.fixture
def status_code():
    return 201


@pytest.fixture
def response(body, status_code):
    return Response(body, status_code)


def test_response(response, body, status_code):
    assert response.body == body
    assert response.status_code == status_code


def test_render_body(response, body):
    rendered_body = response.render_body()

    assert rendered_body == body.encode('utf-8')


@pytest.mark.asyncio
async def test_send_response(response):
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
        call({"type": "http.response.body", "body": response.render_body()}),
    ]

    send = AsyncMock()

    await response(dict(), AsyncMock(), send)

    assert send.await_count == 2
    send.assert_has_awaits(calls)
