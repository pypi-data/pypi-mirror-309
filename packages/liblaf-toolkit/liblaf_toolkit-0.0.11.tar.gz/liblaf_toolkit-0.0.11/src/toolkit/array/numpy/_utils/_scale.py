from __future__ import annotations

from typing import Annotated

import numpy as np
import numpy.typing as npt

import toolkit.validation as tv


@tv.validate_call()
def scale(
    x: Annotated[npt.NDArray, tv.Numpy], a: float = 0, b: float = 1
) -> npt.NDArray:
    x = (x - x.min()) / np.ptp(x)
    x = x * (b - a) + a
    return x
