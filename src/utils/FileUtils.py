from pathlib import Path
from typing import List

from src.utils import Utils


def loadFileAsString(path: Path, errorMessage: str) -> str:
    with open(path) as file:
        try:
            return file.read().strip()
        except Exception as e:
            Utils.exitWithException(errorMessage, e)


def loadFileAsList(path: Path, errorMessage: str) -> List[str]:
    with open(path) as file:
        try:
            return file.readlines()
        except Exception as e:
            Utils.exitWithException(errorMessage, e)


def writeToFile(path: Path, content: str, errorMessage: str):
    try:
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as file:
            file.write(content)
    except Exception as e:
        Utils.exitWithException(errorMessage, e)
