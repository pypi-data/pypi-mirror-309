from collections.abc import Callable
from pathlib import Path
from typing import Any

import toolkit._serialization as _ser
import toolkit.typing as tp

_READERS: dict[str, Callable[..., Any]] = {
    ".json": _ser.load_json,
    ".toml": _ser.load_toml,
    ".yaml": _ser.load_yaml,
}


_WRITERS: dict[str, Callable[..., None]] = {
    ".json": _ser.save_json,
    ".toml": _ser.save_toml,
    ".yaml": _ser.save_yaml,
}


def serialize(fpath: tp.StrPath, *, ext: str | None = None) -> Any:
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in _READERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    reader = _READERS[ext]
    return reader(fpath)


def deserialize(fpath: tp.StrPath, data: Any, *, ext: str | None = None) -> None:
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in _WRITERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    writer = _WRITERS[ext]
    fpath.parent.mkdir(parents=True, exist_ok=True)
    writer(fpath, data)
