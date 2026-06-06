from __future__ import annotations

import sys

from fates._async import AsyncResult
from fates._err import AsyncErr
from tests.func import async_sum, async_sum_non_empty, sum_non_empty

if sys.version_info >= (3, 11):
    from typing import Final, assert_never, assert_type
else:
    from typing_extensions import Final, assert_never, assert_type


import pytest

from fates import Err, Ok, UnwrapError
from fates._result import Result

nums: Final = [1, 2, 3]
err_nums: Final = Err(nums)


def test_eq() -> None:
    err = Err(1)
    assert err == Err(1)
    assert err != Err(2)
    assert err != Ok(1)
    assert err != Ok(2)


def test_unwrap() -> None:
    with pytest.raises(UnwrapError, match=r"[1, 2, 3]"):
        assert_never(err_nums.unwrap())
    with pytest.raises(
        UnwrapError,
        check=lambda exc: exc.__cause__.__class__ is ValueError,
    ):
        assert_never(Err(ValueError()).unwrap())


def test_unwrap_err() -> None:
    res = err_nums.unwrap_err()
    assert_type(res, list[int])
    assert res is nums


def test_unwrap_or() -> None:
    res = Err(1).unwrap_or(nums)
    assert_type(res, list[int])
    assert res is nums


def test_expect() -> None:
    with pytest.raises(UnwrapError, match="note"):
        assert_never(Err(1).expect("note"))
    with pytest.raises(
        UnwrapError,
        check=lambda exc: exc.__cause__.__class__ is ValueError,
        match="blablab",
    ):
        assert_never(Err(ValueError()).expect("blablab"))


def test_resolve() -> None:
    res = err_nums.resolve(sum)
    assert_type(res, int)
    assert res == 6


def test_map() -> None:
    res = err_nums.map(sum)
    assert_type(res, Err[list[int]])
    assert res is err_nums


def test_map_err() -> None:
    res = err_nums.map_err(sum)
    assert_type(res, Err[int])
    assert res == Err(6)


def test_bind() -> None:
    res = err_nums.bind(Ok)
    assert_type(res, Err[list[int]])
    assert res is err_nums


def test_catch() -> None:
    res = err_nums.catch(sum_non_empty)
    assert_type(res, Result[int, str])
    assert res == Ok(6)


async def test_aresolve() -> None:
    res = await err_nums.aresolve(async_sum)
    assert_type(res, int)
    assert res == 6


async def test_amap() -> None:
    res = err_nums.amap(async_sum)
    assert_type(res, AsyncErr[list[int]])
    assert_type(await res, Err[list[int]])
    assert await res is err_nums


async def test_amap_err() -> None:
    res = err_nums.amap_err(async_sum)
    assert_type(res, AsyncErr[int])
    assert_type(await res, Err[int])
    assert await res == Err(6)


async def test_abind() -> None:
    res = err_nums.abind(async_sum_non_empty)
    assert_type(res, AsyncErr[list[int]])
    assert_type(await res, Err[list[int]])
    assert await res is err_nums


async def test_acatch() -> None:
    res = err_nums.acatch(async_sum_non_empty)
    assert_type(res, AsyncResult[int, str])
    assert_type(await res, Result[int, str])
    assert await res == Ok(6)
