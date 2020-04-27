from json import JSONDecodeError

from Ancalagon import App
from Ancalagon.responses import JSONResponse, Response


async def info_middleware(handler, request):
    print('[INFO] : I am info_middleware and I do nothing')
    return await handler(request)


async def response_middleware(handler, request):
    response = await handler(request)
    print(f'[INFO] : response: {response.render_body()}')
    return response


async def validation_middleware(handler, request):
    try:
        json_body = await request.json()
    except JSONDecodeError:
        print('[ERROR] : BAD JSON')
        response = Response(status_code=400)
    else:
        print(f'[INFO] : JSON : valid JSON {json_body}')
        response = await handler(request)

    return response


async def hello(request):
    """
    This route will be checked with this middlewares:
    info_middleware (app middlewares)
    response_middleware (personal route middleware)

    ignored:
    validation_middleware (ignore_middlewares param of this route)
    """

    return JSONResponse({'name': 'Melkor'})


async def world(request):
    """
    This route will be checked with this middlewares:
    info_middleware (app middlewares)
    validation_middleware (app middlewares)
    """

    payload = await request.json()
    return Response(f'<h1>Your JSON: </h1> {payload}')


app = App(middlewares=[info_middleware, validation_middleware])
app.route(
    '/',
    hello,
    ignore_middlewares=[validation_middleware],
    middlewares=[response_middleware]
)
app.route('/echo', world, ['POST'])
