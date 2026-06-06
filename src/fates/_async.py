from __future__ import annotations

from asyncio import ensure_future
from typing import TYPE_CHECKING, Generic, cast

from fates._typevars import DefaultT, E_co, NewE, NewT, T_co

if TYPE_CHECKING:
    from asyncio import Task
    from collections.abc import Awaitable, Generator

    from fates._result import Result
    from fates._types import AsyncBinder, AsyncMapper, Binder, Mapper


class AsyncResult(Generic[T_co, E_co]):
    def __init__(self, awaitable: Awaitable[Result[T_co, E_co]]) -> None:
        self._awaitable = awaitable
        self._cached_task: Task[Result[T_co, E_co]] | None = None

    def __await__(self) -> Generator[object, None, Result[T_co, E_co]]:
        if self._cached_task is None:
            self._cached_task = ensure_future(self._awaitable)
        return self._cached_task.__await__()

    async def unwrap(self) -> T_co:
        res = await self
        return res.unwrap()

    async def unwrap_or(self, default: DefaultT) -> T_co | DefaultT:
        res = await self
        return res.unwrap_or(default)

    async def unwrap_err(self) -> E_co:
        res = await self
        return res.unwrap_err()

    async def expect(self, note: str) -> T_co:
        res = await self
        return res.expect(note)

    def map(self, mapper: Mapper[T_co, NewT]) -> AsyncResult[NewT, E_co]:
        return AsyncResult(self._map(mapper))

    def map_err(self, mapper: Mapper[E_co, NewE]) -> AsyncResult[T_co, NewE]:
        return AsyncResult(self._map_err(mapper))

    def bind(
        self,
        binder: Binder[T_co, NewT, NewE],
    ) -> AsyncResult[NewT, E_co | NewE]:
        return AsyncResult(self._bind(binder))

    def catch(
        self, binder: Binder[E_co, NewT, NewE]
    ) -> AsyncResult[NewT, NewE] | AsyncResult[T_co, E_co]:
        return cast(
            "AsyncResult[T_co, E_co] | AsyncResult[NewT, NewE]",
            AsyncResult(self._catch(binder)),
        )

    async def resolve(self, mapper: Mapper[E_co, NewT]) -> T_co | NewT:
        res = await self
        return res.resolve(mapper)

    def amap(self, mapper: AsyncMapper[T_co, NewT]) -> AsyncResult[NewT, E_co]:
        return AsyncResult(self._amap(mapper))

    def amap_err(self, mapper: AsyncMapper[E_co, NewE]) -> AsyncResult[T_co, NewE]:
        return AsyncResult(self._amap_err(mapper))

    def abind(
        self, binder: AsyncBinder[T_co, NewT, NewE]
    ) -> AsyncResult[NewT, E_co | NewE]:
        return AsyncResult(self._abind(binder))

    def acatch(
        self, binder: AsyncBinder[E_co, NewT, NewE]
    ) -> AsyncResult[T_co, E_co] | AsyncResult[NewT, NewE]:
        return cast(
            "AsyncResult[T_co, E_co] | AsyncResult[NewT, NewE]",
            AsyncResult(self._acatch(binder)),
        )

    async def aresolve(self, mapper: AsyncMapper[E_co, NewT]) -> T_co | NewT:
        res = await self
        return await res.aresolve(mapper)

    async def _catch(
        self, binder: Binder[E_co, NewT, NewE]
    ) -> Result[T_co, E_co] | Result[NewT, NewE]:
        res = await self
        return res.catch(binder)

    async def _acatch(
        self, binder: AsyncBinder[E_co, NewT, NewE]
    ) -> Result[T_co, E_co] | Result[NewT, NewE]:
        res = await self
        return await res.acatch(binder)  # ty: ignore[invalid-return-type]

    async def _map(self, mapper: Mapper[T_co, NewT]) -> Result[NewT, E_co]:
        res = await self
        return res.map(mapper)

    async def _map_err(self, mapper: Mapper[E_co, NewE]) -> Result[T_co, NewE]:
        res = await self
        return res.map_err(mapper)

    async def _bind(
        self, binder: Binder[T_co, NewT, NewE]
    ) -> Result[NewT, E_co | NewE]:
        res = await self
        return res.bind(binder)

    async def _amap(self, mapper: AsyncMapper[T_co, NewT]) -> Result[NewT, E_co]:
        res = await self
        return await res.amap(mapper)

    async def _amap_err(self, mapper: AsyncMapper[E_co, NewE]) -> Result[T_co, NewE]:
        res = await self
        return await res.amap_err(mapper)

    async def _abind(
        self, binder: AsyncBinder[T_co, NewT, NewE]
    ) -> Result[NewT, E_co | NewE]:
        res = await self
        return await res.abind(binder)
