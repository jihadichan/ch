from pathlib import Path

from src.utils import Utils


def top10kHanziFreqList() -> Path:
    path = Path("uberhanzi/resources/top10k_freq_list.csv")
    if not path.exists():
        Utils.exitWithError(f"Failed to find expected file at: {path.absolute()}")
    return path


def hanziList() -> Path:
    path = Path("uberhanzi/resources/hanzi_list.csv")
    if not path.exists():
        Utils.exitWithError(f"Failed to find expected file at: {path.absolute()}")
    return path


def pinyinList() -> Path:
    path = Path("uberhanzi/resources/pinyin.csv")
    if not path.exists():
        Utils.exitWithError(f"Failed to find expected file at: {path.absolute()}")
    return path


def radicalsList() -> Path:
    path = Path("uberhanzi/resources/radicals.csv")
    if not path.exists():
        Utils.exitWithError(f"Failed to find expected file at: {path.absolute()}")
    return path


def pinyinMp3Dir() -> Path:
    path = Path("uberhanzi/pinyin")
    if not path.exists():
        Utils.exitWithError(f"Failed to find pinyin mp3 dir at: {path.absolute()}")
    return path


def hanziCharJsonDir() -> Path:
    path = Path("uberhanzi/hanzi")
    if not path.exists():
        Utils.exitWithError(f"Failed to find hanzi dir at: {path.absolute()}")
    return path
