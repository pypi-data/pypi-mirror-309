from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

import toolkit as tk
import toolkit.typing as tp


def as_numpy(obj: Any) -> np.ndarray:
    if tk.is_numpy(obj):
        return obj
    if tk.is_torch(obj):
        return obj.numpy(force=True)
    return np.asarray(obj)


def as_dict_of_numpy(obj: Mapping[str, tp.ArrayLike] | None) -> dict[str, np.ndarray]:
    if obj is None:
        return {}
    return {k: tk.as_numpy(v) for k, v in obj.items()}
