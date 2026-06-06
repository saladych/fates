from __future__ import annotations

import sys

from tests.func import async_sum, async_sum_non_empty, sum_non_empty

if sys.version_info >= (3, 11):
    from typing import Final, assert_never, assert_type
else:
    from typing_extensions import Final, assert_never, assert_type

import pytest

from fates import Err, Ok, UnwrapError
from fates._async import AsyncResult
from fates._err import AsyncErr


async def nums_res(nums: list[int]) -> Err[list[int]]:
    return Err(nums)


nums: Final = [1, 2, 3]
err_nums: Final = AsyncErr(nums_res(nums))


async def test_unwrap() -> None:
    with pytest.raises(UnwrapError):
        assert_never(await err_nums.unwrap())


async def test_unwrap_or() -> None:
    default = ["2", "3", "4"]
    res = await err_nums.unwrap_or(default)
    assert_type(res, list[str])
    assert res is default


async def test_unwrap_err() -> None:
    res = await err_nums.unwrap_err()
    assert_type(res, list[int])
    assert res is nums


async def test_expect() -> None:
    with pytest.raises(UnwrapError, match="note"):
        assert_never(await err_nums.expect("note"))


def test_map() -> None:
    res = err_nums.map(sum)
    assert_type(res, AsyncErr[list[int]])
    assert res is err_nums


def test_amap() -> None:
    res = err_nums.amap(async_sum)
    assert_type(res, AsyncErr[list[int]])
    assert res is err_nums


async def test_map_err() -> None:
    res = err_nums.map_err(sum)
    assert_type(res, AsyncErr[int])
    assert res.__class__ is AsyncErr
    assert await res == Err(6)


async def test_amap_err() -> None:
    res = err_nums.amap_err(async_sum)
    assert_type(res, AsyncErr[int])
    assert res.__class__ is AsyncErr
    assert await res == Err(6)


async def test_resolve() -> None:
    res = await err_nums.resolve(sum)
    assert_type(res, int)
    assert res == 6


async def test_aresolve() -> None:
    res = await err_nums.aresolve(async_sum)
    assert_type(res, int)
    assert res == 6


def test_bind() -> None:
    res = err_nums.bind(sum_non_empty)
    assert_type(res, AsyncErr[list[int]])
    assert res is err_nums


def test_abind() -> None:
    res = err_nums.abind(async_sum_non_empty)
    assert_type(res, AsyncErr[list[int]])
    assert res is err_nums


async def test_catch() -> None:
    res = err_nums.catch(sum_non_empty)
    assert_type(res, AsyncResult[int, str])
    assert res.__class__ is AsyncResult
    assert await res == Ok(6)


async def test_acatch() -> None:
    res = err_nums.acatch(async_sum_non_empty)
    assert_type(res, AsyncResult[int, str])
    assert res.__class__ is AsyncResult
    assert await res == Ok(6)
