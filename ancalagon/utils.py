import asyncio
import pprint
from functools import partial

pretty_format = pprint.PrettyPrinter(indent=2).pformat


async def run_in_executor(func, *args, **kwargs):
    if kwargs:
        func = partial(func, **kwargs)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


async def run_func(func, *args, **kwargs):
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)

    return await run_in_executor(func, *args, **kwargs)
