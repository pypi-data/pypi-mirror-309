from __future__ import annotations

from typing import Annotated

import numpy as np
import pydantic

import toolkit.validation as tv


@pydantic.validate_call
def scale(x: Annotated[np.ndarray, tv.Numpy], a: float = 0, b: float = 1) -> np.ndarray:
    x = (x - x.min()) / np.ptp(x)
    x = x * (b - a) + a
    return x
