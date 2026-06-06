# pragma: exclude file

import sys
from collections.abc import Awaitable, Callable

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from fates._result import Result
from fates._typevars import New, NewE, NewT, Old, T_co

Mapper: TypeAlias = Callable[[Old], New]

AsyncMapper: TypeAlias = Callable[[Old], Awaitable[New]]

Binder: TypeAlias = Callable[[T_co], Result[NewT, NewE]]

AsyncBinder: TypeAlias = Callable[[T_co], Awaitable[Result[NewT, NewE]]]
