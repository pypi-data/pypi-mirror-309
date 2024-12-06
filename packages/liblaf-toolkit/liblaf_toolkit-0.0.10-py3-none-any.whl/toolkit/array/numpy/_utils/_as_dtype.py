from __future__ import annotations

from typing import Annotated

import numpy as np
import numpy.typing as npt
import pydantic

import toolkit as tk
import toolkit.validation as tv


@tv.validate_call()
def as_dtype(
    x: Annotated[npt.NDArray, tv.Numpy],
    dtype: Annotated[np.dtype, pydantic.BeforeValidator(np.dtype)],
) -> npt.NDArray:
    if np.issubdtype(x.dtype, dtype):
        return x
    if np.isdtype(dtype, "bool"):
        if np.ptp(x) > 0:
            x = tk.array.numpy.scale(x)
        return x > 0.5
    if np.isdtype(dtype, "integral"):
        x = np.rint(x)
    return x.astype(dtype)
