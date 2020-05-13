import json

import pytest

from ancalagon.responses import JSONResponse


@pytest.fixture
def body():
    return {'Melkor': 'Grond'}


def dumps(body):
    return json.dumps(
        body,
        ensure_ascii=False,
        allow_nan=False,
        indent=None,
        separators=(',', ':'),
    ).encode('utf-8')


def test_render_body(body):
    response = JSONResponse(body)

    assert response.render_body() == dumps(body)
