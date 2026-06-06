"""fates — A generic Result[T, E] type for explicit error propagation."""

from fates._err import Err as Err
from fates._ok import Ok as Ok
from fates._result import Result as Result
from fates.exceptions import UnwrapError as UnwrapError
