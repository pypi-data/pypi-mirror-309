import abc
import collections
import collections.abc
from typing import TypeVar, overload

import toolkit.typing as tp

_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)


class Mapping(collections.abc.Mapping[_KT, _VT_co]):
    @overload
    def __getitem__(self, key: _KT) -> _VT_co: ...
    @overload
    def __getitem__(self, key: collections.abc.Iterable[_KT]) -> list[_VT_co]: ...
    def __getitem__(
        self, key: _KT | collections.abc.Iterable[_KT]
    ) -> _VT_co | list[_VT_co]:
        if tp.is_iterable(key):
            return [self._get(k) for k in key]
        return self._get(key)  # pyright: ignore [reportArgumentType]

    @abc.abstractmethod
    def _get(self, key: _KT) -> _VT_co: ...
