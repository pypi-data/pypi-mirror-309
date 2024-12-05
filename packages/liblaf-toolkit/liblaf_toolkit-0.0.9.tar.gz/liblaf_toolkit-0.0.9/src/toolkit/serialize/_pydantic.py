from typing import Any, TypeVar

import pydantic

import toolkit as tk
import toolkit.typing as tp

_C = TypeVar("_C", bound=pydantic.BaseModel)


def load_pydantic(fpath: tp.StrPath, cls: type[_C], *, ext: str | None = None) -> _C:
    data: Any = tk.serialize.load(fpath, ext=ext)
    return cls.model_validate(data)


def save_pydantic(
    fpath: tp.StrPath, data: pydantic.BaseModel, *, ext: str | None = None
) -> None:
    tk.serialize.save(fpath, data.model_dump(), ext=ext)
