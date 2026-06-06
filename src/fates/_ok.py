from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Awaitable, Generator, cast, final

if sys.version_info >= (3, 12):
    from typing import Never, Self, override  # pragma: no cover
else:
    from typing_extensions import Never, Self, override  # pragma: no cover


from fates._async import AsyncResult
from fates._result import Result
from fates._typevars import NewE, NewT, T_co
from fates.exceptions import UnwrapError

if TYPE_CHECKING:
    from fates._types import AsyncBinder, AsyncMapper, Binder, Mapper


@final
class Ok(Result[T_co, Never]):
    __slots__ = ("_boxed_val",)
    __match_args__ = ("_boxed_val",)

    def __init__(self, boxed_val: T_co) -> None:
        self._boxed_val = boxed_val

    def __repr__(self) -> str:
        return f"Ok({self._boxed_val!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            other = cast("Ok[object]", other)  # ty: ignore[redundant-cast]
            return self._boxed_val == other._boxed_val
        return False

    def __hash__(self) -> int:
        return self._boxed_val.__hash__()  # pragma: no cover

    @override
    def unwrap(self) -> T_co:
        return self._boxed_val

    @override
    def unwrap_or(self, default: object) -> T_co:
        return self._boxed_val

    @override
    def unwrap_err(self) -> Never:
        msg = f"unwrap_err() called on {self}"
        raise UnwrapError(msg)

    @override
    def expect(self, note: str) -> T_co:
        return self._boxed_val

    @override
    def map(self, mapper: Mapper[T_co, NewT]) -> Ok[NewT]:
        return Ok(mapper(self._boxed_val))

    @override
    def map_err(self, mapper: Mapper[Never, object]) -> Self:
        return self

    @override
    def bind(self, binder: Binder[T_co, NewT, NewE]) -> Result[NewT, NewE]:
        return binder(self._boxed_val)

    @override
    def catch(self, binder: Binder[Never, object, object]) -> Self:
        return self

    @override
    def resolve(self, mapper: Mapper[Never, object]) -> T_co:
        return self._boxed_val

    @override
    def amap(self, mapper: AsyncMapper[T_co, NewT]) -> AsyncOk[NewT]:
        return AsyncOk(self._async_map(mapper))

    @override
    def amap_err(self, mapper: AsyncMapper[Never, object]) -> AsyncOk[T_co]:
        return AsyncOk(self._return_self())

    @override
    def abind(self, binder: AsyncBinder[T_co, NewT, NewE]) -> AsyncResult[NewT, NewE]:
        return AsyncResult(self._async_bind(binder))

    @override
    def acatch(self, binder: AsyncBinder[Never, object, object]) -> AsyncOk[T_co]:
        return AsyncOk(self._return_self())

    @override
    async def aresolve(self, mapper: AsyncMapper[Never, object]) -> T_co:
        return self._boxed_val

    async def _async_map(self, mapper: AsyncMapper[T_co, NewT]) -> Ok[NewT]:
        return Ok(await mapper(self._boxed_val))

    async def _async_bind(
        self, binder: AsyncBinder[T_co, NewT, NewE]
    ) -> Result[NewT, NewE]:
        return await binder(self._boxed_val)

    async def _return_self(self) -> Self:
        return self


@final
class AsyncOk(AsyncResult[T_co, Never]):
    @override
    def __init__(self, awaitable: Awaitable[Ok[T_co]]) -> None:
        super().__init__(awaitable)

    @override
    def __await__(self) -> Generator[object, None, Ok[T_co]]:
        return cast("Generator[object, None, Ok[T_co]]", super().__await__())

    @override
    async def unwrap_or(self, default: object) -> T_co:
        res = await self
        return res.unwrap()

    @override
    async def expect(self, note: str) -> T_co:
        res = await self
        return res.unwrap()

    @override
    async def resolve(self, mapper: Mapper[Never, object]) -> T_co:
        res = await self
        return res.unwrap()

    @override
    async def aresolve(self, mapper: AsyncMapper[Never, object]) -> T_co:
        res = await self
        return res.unwrap()

    @override
    def map(self, mapper: Mapper[T_co, NewT]) -> AsyncOk[NewT]:
        return AsyncOk(self._map(mapper))

    @override
    def amap(self, mapper: AsyncMapper[T_co, NewT]) -> AsyncOk[NewT]:
        return AsyncOk(self._amap(mapper))

    @override
    def map_err(self, mapper: Mapper[Never, object]) -> Self:
        return self

    @override
    def catch(self, binder: Binder[Never, object, object]) -> Self:
        return self

    @override
    def acatch(self, binder: AsyncBinder[Never, object, object]) -> Self:
        return self

    @override
    def amap_err(self, mapper: AsyncMapper[Never, object]) -> Self:
        return self

    @override
    async def _map(self, mapper: Mapper[T_co, NewT]) -> Ok[NewT]:
        res = await self
        return res.map(mapper)

    @override
    async def _amap(self, mapper: AsyncMapper[T_co, NewT]) -> Ok[NewT]:
        res = await self
        return await res.amap(mapper)
