from Ancalagon import App
from Ancalagon.responses import JSONResponse, Response


async def hello(request):
    request.headers
    request.headers
    return JSONResponse({'name': 'Melkor'})


async def world(request):
    payload = await request.json()
    return Response(f'<h1>Your JSON: </h1> {payload}')


async def start(app):
    print('starting')


async def stop():
    with open('/home/dnomin/dev/Ancalagon/blyad.txt', 'wb') as f:
        f.write('suka')

    print('stopping')
    return 'lol'


app = App(debug=True, startup=[start], shutdown=[stop])
app.route('/', hello)
app.route('/echo', world, ['POST'])
