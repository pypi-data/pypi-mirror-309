from collections.abc import Callable
from pathlib import Path
from typing import Any

import toolkit as tk
import toolkit.typing as tp

_READERS: dict[str, Callable[..., Any]] = {
    ".json": tk.serialize.load_json,
    ".toml": tk.serialize.load_toml,
    ".yaml": tk.serialize.load_yaml,
}


_WRITERS: dict[str, Callable[..., None]] = {
    ".json": tk.serialize.save_json,
    ".toml": tk.serialize.save_toml,
    ".yaml": tk.serialize.save_yaml,
}


def load(fpath: tp.StrPath, *, ext: str | None = None) -> Any:
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in _READERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    reader = _READERS[ext]
    return reader(fpath)


def save(fpath: tp.StrPath, data: Any, *, ext: str | None = None) -> None:
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in _WRITERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    writer = _WRITERS[ext]
    fpath.parent.mkdir(parents=True, exist_ok=True)
    writer(fpath, data)
