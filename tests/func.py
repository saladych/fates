from __future__ import annotations

from fates import Err, Ok, Result


def sum_non_empty(nums: list[int]) -> Result[int, str]:
    if len(nums) > 0:
        return Ok(sum(nums))
    return Err("empty")


async def async_sum_non_empty(nums: list[int]) -> Result[int, str]:
    if len(nums) > 0:
        return Ok(sum(nums))
    return Err("empty")


async def async_sum(nums: list[int]) -> int:
    return sum(nums)
