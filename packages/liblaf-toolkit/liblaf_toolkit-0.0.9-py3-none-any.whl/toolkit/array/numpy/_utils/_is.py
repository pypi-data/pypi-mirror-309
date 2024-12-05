from __future__ import annotations

from typing import Any, TypeGuard

import numpy as np

import toolkit.typing as tp


def is_numpy(obj: Any) -> TypeGuard[np.ndarray]:
    return tp.is_instance_named_partial(obj, "numpy.ndarray")
