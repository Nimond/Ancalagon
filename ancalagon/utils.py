import asyncio
import pprint
from functools import partial
from typing import Any, Callable, Awaitable, Union

pretty_format = pprint.PrettyPrinter(indent=2).pformat


async def run_in_executor(
    func: Callable[..., Union[Awaitable[Any], Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    if kwargs:
        func = partial(func, **kwargs)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)


async def run_func(
    func: Callable[..., Union[Awaitable[Any], Any]],
    *args: Any,
    **kwargs: Any,
) -> Any:
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)

    return await run_in_executor(func, *args, **kwargs)
