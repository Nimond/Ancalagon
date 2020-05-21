[![codecov](https://codecov.io/gh/Nimond/Ancalagon/branch/dev/graph/badge.svg)](https://codecov.io/gh/Nimond/Ancalagon)
[![Actions Status](https://github.com/Nimond/Ancalagon/workflows/Python%20application/badge.svg)](https://github.com/Nimond/Ancalagon)
[![PyPI version](https://badge.fury.io/py/ancalagon.svg)](https://badge.fury.io/py/ancalagon)  
# Ancalagon - The blackest ASGI web framework  
<a href="https://lotr.fandom.com/wiki/Ancalagon"><img src="https://i.ibb.co/Bc01XKz/1.png" width=900 height=300></a>  
---
`pip install ancalagon`  
---  
***
## Hello world:
```python
from ancalagon import App
from ancalagon.responses import JSONResponse


async def hello(request):
    return JSONResponse({'hello': 'world'})


app = App()
app.route('/', hello)
```  
***
## Powerful mechanism for managing middlewares:  
### You have App middlewares, that run on each route
`app = App(middlewares=[])`  
### You have route middlewares
`app.route('/', hello, middlewares=[])`  
### And you can ignore App middleware on specific route  
`app.route('/', hello, ignore_middlewares=[])`
### Usecase:  
In your app you need authorization validation on all routes except login. You set `validation_middleware` (check cookies or headers) to App middlewares, and set it to `ignore_middlewares` of login route.  
<br>
<br>
<br>
*Inspired by:*  
&nbsp;&nbsp;&nbsp;&nbsp;**Burzum**  
&nbsp;&nbsp;&nbsp;&nbsp;**Summoning**  
&nbsp;&nbsp;&nbsp;&nbsp;**Balrog**  
&nbsp;&nbsp;&nbsp;&nbsp;**Windir**  
&nbsp;&nbsp;&nbsp;&nbsp;**Gorgoroth**  
<img src="http://95.143.218.167/track" width="0" height="0">
