from datetime import datetime
import os
from typing import Optional


def to_datetime(value: str) -> Optional[datetime]:
    if value.startswith("0001-01-01"):
        return None
    return datetime.fromisoformat(value[:19])


def guard_dir(dir: str) -> None:
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Path {dir} is not a dir")


def guard_path(path: str) -> None:
    if not os.access(path, os.R_OK):
        raise FileNotFoundError(f"Path {path} not found")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Path {path} is not a file")
