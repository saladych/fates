from typing import TypeVar

T_co = TypeVar("T_co", covariant=True)
E_co = TypeVar("E_co", covariant=True)
NewT = TypeVar("NewT")
NewE = TypeVar("NewE")
DefaultT = TypeVar("DefaultT")
Old = TypeVar("Old")
New = TypeVar("New")
