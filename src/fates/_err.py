from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Awaitable, cast, final

if sys.version_info >= (3, 12):
    from typing import Never, Self, override  # pragma: no cover
else:
    from typing_extensions import Never, Self, override  # pragma: no cover


from fates._async import AsyncResult
from fates._result import Result
from fates._typevars import DefaultT, E_co, NewE, NewT
from fates.exceptions import UnwrapError

if TYPE_CHECKING:
    from collections.abc import Generator

    from fates._types import AsyncBinder, AsyncMapper, Binder, Mapper


@final
class Err(Result[Never, E_co]):
    __slots__ = ("_boxed_err",)
    __match_args__ = ("_boxed_err",)

    def __init__(self, boxed_err: E_co) -> None:
        self._boxed_err = boxed_err

    def __repr__(self) -> str:
        return f"Err({self._boxed_err!r})"

    def __hash__(self) -> int:
        return self._boxed_err.__hash__()  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            other = cast("Err[object]", other)  # ty: ignore[redundant-cast]
            return self._boxed_err == other._boxed_err
        return False

    @override
    def unwrap(self) -> Never:
        err = UnwrapError(repr(self._boxed_err))
        if isinstance(self._boxed_err, BaseException):
            raise err from self._boxed_err
        raise err

    @override
    def unwrap_or(self, default: DefaultT) -> DefaultT:
        return default

    @override
    def unwrap_err(self) -> E_co:
        return self._boxed_err

    @override
    def expect(self, note: str) -> Never:
        err_msg = f"{note}\nError details: {self._boxed_err!r}"
        err = UnwrapError(err_msg)
        if isinstance(self._boxed_err, BaseException):
            raise err from self._boxed_err
        raise err

    @override
    def map(self, mapper: Mapper[Never, object]) -> Self:
        return self

    @override
    def map_err(self, mapper: Mapper[E_co, NewE]) -> Err[NewE]:
        return Err(mapper(self._boxed_err))

    @override
    def bind(
        self,
        binder: Binder[Never, object, object],
    ) -> Self:
        return self

    @override
    def catch(self, binder: Binder[E_co, NewT, NewE]) -> Result[NewT, NewE]:
        return binder(self._boxed_err)

    @override
    def resolve(self, mapper: Mapper[E_co, NewT]) -> NewT:
        return mapper(self._boxed_err)

    @override
    def amap(self, mapper: AsyncMapper[Never, object]) -> AsyncErr[E_co]:
        return AsyncErr(self._return_self())

    @override
    def amap_err(self, mapper: AsyncMapper[E_co, NewE]) -> AsyncErr[NewE]:
        return AsyncErr(self._async_map_err(mapper))

    @override
    def abind(self, binder: AsyncBinder[Never, object, object]) -> AsyncErr[E_co]:
        return AsyncErr(self._return_self())

    @override
    def acatch(self, binder: AsyncBinder[E_co, NewT, NewE]) -> AsyncResult[NewT, NewE]:
        return AsyncResult(self._acatch(binder))

    @override
    async def aresolve(self, mapper: AsyncMapper[E_co, NewT]) -> NewT:
        return await mapper(self._boxed_err)

    async def _return_self(self) -> Self:
        return self

    async def _acatch(
        self, binder: AsyncBinder[E_co, NewT, NewE]
    ) -> Result[NewT, NewE]:
        return await binder(self._boxed_err)

    async def _async_map_err(self, mapper: AsyncMapper[E_co, NewE]) -> Err[NewE]:
        return Err(await mapper(self._boxed_err))


@final
class AsyncErr(AsyncResult[Never, E_co]):
    @override
    def __init__(self, awaitable: Awaitable[Err[E_co]]) -> None:
        super().__init__(awaitable)

    @override
    def __await__(self) -> Generator[object, None, Err[E_co]]:
        return cast("Generator[object, None, Err[E_co]]", super().__await__())

    @override
    def map(self, mapper: Mapper[Never, object]) -> Self:
        return self

    @override
    def amap(self, mapper: AsyncMapper[Never, object]) -> Self:
        return self

    @override
    def bind(self, binder: Binder[Never, object, object]) -> Self:
        return self

    @override
    def abind(self, binder: AsyncBinder[Never, object, object]) -> Self:
        return self

    @override
    def map_err(self, mapper: Mapper[E_co, NewE]) -> AsyncErr[NewE]:
        return AsyncErr(self._map_err(mapper))

    @override
    def amap_err(self, mapper: AsyncMapper[E_co, NewE]) -> AsyncErr[NewE]:
        return AsyncErr(self._amap_err(mapper))

    @override
    def catch(self, binder: Binder[E_co, NewT, NewE]) -> AsyncResult[NewT, NewE]:
        return AsyncResult(self._catch(binder))

    @override
    def acatch(self, binder: AsyncBinder[E_co, NewT, NewE]) -> AsyncResult[NewT, NewE]:
        return AsyncResult(self._acatch(binder))

    @override
    async def _map_err(self, mapper: Mapper[E_co, NewE]) -> Err[NewE]:
        res = await self
        return res.map_err(mapper)

    @override
    async def _amap_err(self, mapper: AsyncMapper[E_co, NewE]) -> Err[NewE]:
        res = await self
        return await res.amap_err(mapper)

    @override
    async def _catch(self, binder: Binder[E_co, NewT, NewE]) -> Result[NewT, NewE]:
        res = await self
        return res.catch(binder)

    @override
    async def _acatch(
        self, binder: AsyncBinder[E_co, NewT, NewE]
    ) -> Result[NewT, NewE]:
        res = await self
        return await res.acatch(binder)
