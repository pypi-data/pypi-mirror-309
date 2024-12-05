from os import PathLike
from typing import TypeAlias

Scalar: TypeAlias = bool | int | float
StrPath: TypeAlias = str | PathLike[str]


__all__ = [
    "Scalar",
    "StrPath",
]
