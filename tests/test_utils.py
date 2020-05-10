import pytest

from ancalagon.utils import run_func


@pytest.fixture
def n():
    return 2


def func(n):
    return n * n


async def coro_func(n):
    return n * n


@pytest.mark.asyncio
async def test_run_func_coro(n):
    assert await coro_func(n) == await run_func(coro_func, n)


@pytest.mark.asyncio
async def test_run_func_func(n):
    assert func(n) == await run_func(func, n=n)
