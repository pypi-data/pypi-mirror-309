from typing import Any

import toolkit as tk


def as_scalar(x: Any) -> float:
    if tk.is_jax(x):
        return x.item()
    if tk.is_numpy(x):
        return x.item()
    if tk.is_torch(x):
        return x.item()
    return x
