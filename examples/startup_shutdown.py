from ancalagon import App
from ancalagon.responses import JSONResponse


async def hello(request):
    print(request.headers)
    return JSONResponse({'name': 'Melkor'})


async def start(application):
    print('starting')
    # do some startup stuff here
    # e.g. connect to database | rabbitmq


async def end(application):
    print('ending')
    # do some shutdown stuff here
    # e.g. disconnect from database,
    # wait for some jobs are done


app = App(startup=[start], shutdown=[end])
app.route('/', hello)
