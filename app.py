from json import JSONDecodeError

from Ancalagon import App
from Ancalagon.responses import JSONResponse, Response


async def info_middleware(handler, request):
    print(f'[INFO] : PATH : {request.path}')
    response = await handler(request)
    print(f'[INFO] : RESPONSE : {response.status_code}')
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


async def response_middleware(handler, request):
    response = await handler(request)
    print(
        f'[INFO] : RESPONSE : {response.render_body()}, {response.status_code}'
    )
    return response


async def hello(request):
    request.headers
    request.headers
    return JSONResponse({'name': 'Melkor'})


async def world(request):
    print('echoing')
    payload = await request.json()
    return Response(f'<h1>Your JSON: </h1> {payload}')


async def start(app):
    print('starting')


async def end(app):
    print('ending')


app = App(
    startup=[start],
    shutdown=[end],
    middlewares=[info_middleware, validation_middleware]
)
app.route(
    '/',
    hello,
    ignore_middlewares=[validation_middleware],
    middlewares=[response_middleware]
)
app.route('/echo', world, ['POST'])


'''
response_middleware works only for hello route
validation_middleware works only for world route, because it is in ignore_middlewares of hello route

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13814]
INFO:     Started server process [13816]
INFO:     Waiting for application startup.
starting
INFO:     Application startup complete.
[INFO] : PATH : /
[INFO] : RESPONSE : 200
[INFO] : RESPONSE : b'{"name":"Melkor"}', 200
INFO:     127.0.0.1:59552 - "GET / HTTP/1.1" 200 OK  # http :8000/
[INFO] : PATH : /echo
[INFO] : JSON : valid JSON {'name': 'lol'}
echoing
[INFO] : RESPONSE : 200
INFO:     127.0.0.1:59556 - "POST /echo HTTP/1.1" 200 OK  # http :8000/echo name=lol
[INFO] : PATH : /echo
[ERROR] : BAD JSON
[INFO] : RESPONSE : 400
INFO:     127.0.0.1:59560 - "POST /echo HTTP/1.1" 400 Bad Request  # http POST :8000/echo 
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
ending
INFO:     Application shutdown complete.
INFO:     Finished server process [13816]
INFO:     Stopping reloader process [13814]

'''
