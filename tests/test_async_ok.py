from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Final, assert_never, assert_type
else:
    from typing_extensions import Final, assert_never, assert_type

import pytest

from fates import Ok, UnwrapError
from fates._async import AsyncResult
from fates._ok import AsyncOk
from tests.func import async_sum, async_sum_non_empty, sum_non_empty


async def nums_res_ok(nums: list[int]) -> Ok[list[int]]:
    return Ok(nums)


nums: Final = [1, 2, 3]
ok_nums: Final = AsyncOk(nums_res_ok(nums))


async def test_unwrap() -> None:
    res = await ok_nums.unwrap()
    assert_type(res, list[int])
    assert res is nums


async def test_unwrap_or() -> None:
    res = await ok_nums.unwrap_or(1)
    assert_type(res, list[int])
    assert res is nums


async def test_unwrap_err() -> None:
    with pytest.raises(UnwrapError):
        assert_never(await ok_nums.unwrap_err())


async def test_expect() -> None:
    res = await ok_nums.expect("note")
    assert_type(res, list[int])
    assert res is nums


async def test_map() -> None:
    res = ok_nums.map(sum)
    assert_type(res, AsyncOk[int])
    assert res.__class__ is AsyncOk
    assert await res == Ok(6)


def test_map_err() -> None:
    res = ok_nums.map_err(sum)
    assert_type(res, AsyncOk[list[int]])
    assert res is ok_nums


async def test_amap() -> None:
    res = ok_nums.amap(async_sum)
    assert_type(res, AsyncOk[int])
    assert res.__class__ is AsyncOk
    assert await res == Ok(6)


def test_amap_err() -> None:
    res = ok_nums.amap_err(async_sum)
    assert_type(res, AsyncOk[list[int]])
    assert res is ok_nums


def test_catch() -> None:
    res = ok_nums.catch(sum_non_empty)
    assert_type(res, AsyncOk[list[int]])
    assert res is ok_nums


def test_acatch() -> None:
    res = ok_nums.acatch(async_sum_non_empty)
    assert_type(res, AsyncOk[list[int]])
    assert res is ok_nums


async def test_resolve() -> None:
    res = await ok_nums.resolve(sum)
    assert_type(res, list[int])
    assert res is (await ok_nums).unwrap()


async def test_aresolve() -> None:
    res = await ok_nums.aresolve(async_sum)
    assert_type(res, list[int])
    assert res is (await ok_nums).unwrap()


async def test_bind() -> None:
    res = ok_nums.bind(sum_non_empty)
    assert_type(res, AsyncResult[int, str])
    assert res.__class__ is AsyncResult
    assert await res == Ok(6)


async def test_abind() -> None:
    res = ok_nums.abind(async_sum_non_empty)
    assert_type(res, AsyncResult[int, str])
    assert res.__class__ is AsyncResult
    assert await res == Ok(6)
