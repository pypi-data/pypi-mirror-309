from pathlib import Path

import pydantic


def mkdir(x: Path) -> Path:
    x.mkdir(parents=True, exist_ok=True)
    return x


def parent_mkdir(x: Path) -> Path:
    x.parent.mkdir(parents=True, exist_ok=True)
    return x


SaveDirPath = pydantic.AfterValidator(mkdir)
SaveFilePath = pydantic.AfterValidator(parent_mkdir)
