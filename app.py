from Ancalagon import App, Route


async def unnamed_hello(request):
    return 'Hello mfucker'


async def named_hello(request):
    return 'Hello my dear friend ' + request.json['name']


app = App()
app.route(Route('/hello-anon', unnamed_hello))
app.route(Route('/hello-user', named_hello, ['POST']))

"""
╭─ on master +5 !1
╰─ ~/dev/Ancalagon ❯ http :8000/hello-anon
HTTP/1.1 200 OK
content-type: text/plain
date: Thu, 23 Apr 2020 23:07:12 GMT
server: uvicorn
transfer-encoding: chunked

Hello mfucker

╭─ on master +5 !1
╰─ ~/dev/Ancalagon ❯ http :8000/hello-user name=Abu
HTTP/1.1 200 OK
content-type: text/plain
date: Thu, 23 Apr 2020 23:07:30 GMT
server: uvicorn
transfer-encoding: chunked

Hello my dear friend Abu

"""
