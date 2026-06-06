from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Generic, Protocol

from fates._typevars import DefaultT, E_co, NewE, NewT, T_co

if sys.version_info >= (3, 11):
    from typing import Self  # pragma: no cover
else:
    from typing_extensions import Self  # pragma: no cover

if TYPE_CHECKING:
    from fates._async import AsyncResult
    from fates._types import AsyncBinder, AsyncMapper, Binder, Mapper


class Result(Protocol, Generic[T_co, E_co]):
    def unwrap(self) -> T_co:
        """Extracts the success value or raises an exception if it is a failure.

        Returns:
            T_co: The contained success value.

        Raises:
            UnwrapError: If the result is an Err.

        Examples:
            >>> Ok(42).unwrap()
            42
            >>> Err("error").unwrap()
            Traceback (most recent call last):
            fates.exceptions.UnwrapError: 'error'
        """
        ...

    def unwrap_or(self, default: DefaultT) -> T_co | DefaultT:
        """Returns the success value or a default value if it is a failure.

        Args:
            default (DefaultT): The fallback value to return.

        Returns:
            T_co | DefaultT: The contained value or the default value.

        Examples:
            >>> Ok(42).unwrap_or(0)
            42
            >>> Err("error").unwrap_or(0)
            0
        """
        ...

    def unwrap_err(self) -> E_co:
        """Extracts the error value or raises an exception if it is a success.

        Returns:
            E_co: The contained error value.

        Raises:
            UnwrapError: If the result is an Ok.

        Examples:
            >>> Err("danger").unwrap_err()
            'danger'
            >>> Ok(42).unwrap_err()
            Traceback (most recent call last):
            fates.exceptions.UnwrapError: unwrap_err() called on Ok(42)
        """
        ...

    def expect(self, note: str) -> T_co:
        """Extracts the value or raises an exception with a custom message.

        Args:
            note (str): The custom error message to include in the exception.

        Returns:
            T_co: The contained success value.

        Raises:
            UnwrapError: If the result is an Err, containing the note.

        Examples:
            >>> Ok(42).expect("Should be a number")
            42
            >>> Err("db_error").expect("Database connection failed")
            Traceback (most recent call last):
            fates.exceptions.UnwrapError: Database connection failed
            Error details: 'db_error'
        """
        ...

    def map(
        self,
        mapper: Mapper[T_co, NewT],
    ) -> Result[NewT, E_co]:
        """Applies a function to the success value, leaving an error untouched.

        Args:
            mapper (Mapper[T_co, NewT]): A function to transform the success value.

        Returns:
            Result[NewT, E_co]: A new Result with
                the transformed value or original error.

        Examples:
            >>> Ok(2).map(lambda x: x * 2)
            Ok(4)
            >>> Err("error").map(lambda x: x * 2)
            Err('error')
        """
        ...

    def map_err(
        self,
        mapper: Mapper[E_co, NewE],
    ) -> Result[T_co, NewE]:
        """Applies a function to the error value, leaving a success untouched.

        Args:
            mapper (Mapper[E_co, NewE]): A function to transform the error value.

        Returns:
            Result[T_co, NewE]: A new Result with the
                transformed error or original value.

        Examples:
            >>> Err("failed").map_err(lambda e: f"Log: {e}")
            Err('Log: failed')
            >>> Ok(42).map_err(lambda e: f"Log: {e}")
            Ok(42)
        """
        ...

    def bind(
        self,
        binder: Binder[T_co, NewT, NewE],
    ) -> Result[NewT, E_co | NewE]:
        """Monadic bind. Transforms the success value into a new Result.

        Args:
            binder (Binder[T_co, NewT, NewE]): A function that takes the success
                value and returns a new Result.

        Returns:
            Result[NewT, E_co | NewE]: The new Result, or the original Err.

        Examples:
            >>> def check_positive(x: int) -> Result[int, str]:
            ...     return Ok(x) if x > 0 else Err("negative")
            >>> Ok(5).bind(check_positive)
            Ok(5)
            >>> Ok(-1).bind(check_positive)
            Err('negative')
            >>> Err("not_a_number").bind(check_positive)
            Err('not_a_number')
        """
        ...

    def catch(
        self,
        binder: Binder[E_co, NewT, NewE],
    ) -> Self | Result[NewT, NewE]:
        """Handles an error by transforming it into a new Result.

        Args:
            binder (Binder[E_co, NewT, NewE]): A function that takes the error
                value and returns a alternative Result.

        Returns:
            Self | Result[NewT, NewE]: The original Ok,
                or the new Result from the binder.

        Examples:
            >>> def recover(e: str) -> Result[int, str]:
            ...     return Ok(0) if e == "recoverable" else Err("fatal")
            >>> Ok(42).catch(recover)
            Ok(42)
            >>> Err("recoverable").catch(recover)
            Ok(0)
            >>> Err("boom").catch(recover)
            Err('fatal')
        """
        ...

    def resolve(self, mapper: Mapper[E_co, NewT]) -> T_co | NewT:
        """Returns the success value or transforms the error into a success type.

        Args:
            mapper (Mapper[E_co, NewT]): A function to transform the error value.

        Returns:
            T_co | NewT: The original success value or the transformed error value.

        Examples:
            >>> Ok(100).resolve(lambda e: 0)
            100
            >>> Err("missing").resolve(lambda e: 0)
            0
        """
        ...

    def amap(
        self,
        mapper: AsyncMapper[T_co, NewT],
    ) -> AsyncResult[NewT, E_co]:
        """Asynchronously maps the success value using an async function.

        Args:
            mapper (AsyncMapper[T_co, NewT]): An async function to transform the value.

        Returns:
            AsyncResult[NewT, E_co]: An async result wrapper.

        Examples:
            >>> async def async_double(x: int) -> int:
            ...     return x * 2
            >>> await Ok(2).amap(async_double)
            Ok(4)
            >>> await Err("error").amap(async_double)
            Err('error')
        """
        ...

    def amap_err(
        self,
        mapper: AsyncMapper[E_co, NewE],
    ) -> AsyncResult[T_co, NewE]:
        """Asynchronously maps the error value using an async function.

        Args:
            mapper (AsyncMapper[E_co, NewE]): An async function to transform the error.

        Returns:
            AsyncResult[T_co, NewE]: An async result wrapper.

        Examples:
            >>> async def async_log(e: str) -> str:
            ...     return f"logged_{e}"
            >>> await Err("fail").amap_err(async_log)
            Err('logged_fail')
            >>> await Ok(42).amap_err(async_log)
            Ok(42)
        """
        ...

    def abind(
        self, binder: AsyncBinder[T_co, NewT, NewE]
    ) -> AsyncResult[NewT, E_co | NewE]:
        """
        Asynchronously binds the success value to an async
            function returning a Result.

        Args:
            binder (AsyncBinder[T_co, NewT, NewE]): An async
                function returning a Result.

        Returns:
            AsyncResult[NewT, E_co | NewE]: An async result wrapper.

        Examples:
            >>> async def async_check(x: int) -> Result[int, str]:
            ...     return Ok(x) if x > 0 else Err("negative")
            >>> await Ok(5).abind(async_check)
            Ok(5)
            >>> await Err("error").abind(async_check)
            Err('error')
        """
        ...

    def acatch(
        self,
        binder: AsyncBinder[E_co, NewT, NewE],
    ) -> AsyncResult[T_co, E_co] | AsyncResult[NewT, NewE]: ...

    async def aresolve(self, mapper: AsyncMapper[E_co, NewT]) -> T_co | NewT: ...
