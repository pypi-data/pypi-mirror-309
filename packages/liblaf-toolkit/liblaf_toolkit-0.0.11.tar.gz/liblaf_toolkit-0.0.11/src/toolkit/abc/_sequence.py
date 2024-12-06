import abc
import collections.abc
from typing import TypeVar, overload

import toolkit.typing as tp

_T_co = TypeVar("_T_co", covariant=True)


class Sequence(collections.abc.Sequence[_T_co]):
    @overload
    def __getitem__(self, index: int) -> _T_co: ...
    @overload
    def __getitem__(
        self, index: slice | collections.abc.Iterable[int]
    ) -> list[_T_co]: ...
    def __getitem__(
        self, index: int | slice | collections.abc.Iterable[int]
    ) -> _T_co | list[_T_co]:
        if isinstance(index, int):
            return self._get(index)
        if isinstance(index, slice):
            return [self._get(i) for i in range(*index.indices(len(self)))]
        if tp.is_iterable(index):
            return [self._get(i) for i in index]
        return self._get(index)  # pyright: ignore [reportArgumentType]

    @abc.abstractmethod
    def _get(self, idx: int) -> _T_co: ...
