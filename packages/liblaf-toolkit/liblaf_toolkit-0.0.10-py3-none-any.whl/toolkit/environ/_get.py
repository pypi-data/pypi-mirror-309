import os
from typing import overload

import pydantic

bool_adapter: pydantic.TypeAdapter[bool] = pydantic.TypeAdapter(bool)


def get_bool(key: str, default: bool = False) -> bool:  # noqa: FBT001, FBT002
    if val := os.getenv(key):
        return bool_adapter.validate_strings(val)
    return default


@overload
def get_str(key: str) -> str | None: ...
@overload
def get_str(key: str, default: str) -> str: ...
def get_str(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)
