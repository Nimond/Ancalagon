from Ancalagon import App
from Ancalagon.responses import JSONResponse


async def hello(request):
    print(request.headers)
    return JSONResponse({'name': 'Melkor'})


async def start(app):
    print('starting')
    # do some startup stuff here
    # e.g. connect to database | rabbitmq


async def end(app):
    print('ending')
    # do some shutdown stuff here
    # e.g. disconnect from database,
    # wait for some jobs are done


app = App(startup=[start], shutdown=[end])
app.route('/', hello)
