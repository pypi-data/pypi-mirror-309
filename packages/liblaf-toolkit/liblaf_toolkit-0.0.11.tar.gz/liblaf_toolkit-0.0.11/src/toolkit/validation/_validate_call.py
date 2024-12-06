from collections.abc import Callable
from typing import TypeVar

import pydantic

_AnyCallableT = TypeVar("_AnyCallableT", bound=Callable)


def validate_call(
    *, config: pydantic.ConfigDict | None = None, validate_return: bool = True
) -> Callable[[_AnyCallableT], _AnyCallableT]:
    if config is None:
        config = pydantic.ConfigDict(
            arbitrary_types_allowed=True,
            validate_default=True,
            validate_return=validate_return,
        )
    return pydantic.validate_call(config=config, validate_return=validate_return)
