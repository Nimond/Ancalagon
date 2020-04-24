from Ancalagon import App
from Ancalagon.responses import JSONResponse, Response


async def hello(request):
    return JSONResponse({'name': 'Melkor'})


async def world(request):
    payload = await request.json()
    return Response(f'<h1>Your JSON: </h1> {payload}')


app = App(debug=True)
app.route('/', hello)
app.route('/echo', world, ['POST'])
