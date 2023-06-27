from re import split
from typing import Dict, Optional

from pydantic import BaseModel

from src.commons import FilePaths
from src.models.HanziChar import HanziChar
from src.utils import FileUtils, Utils


class PinyinType:
    ASCII = "ASCII"
    HANYU = "HANYU"


class Pinyin(BaseModel):
    ascii: str
    hanyu: str
    type: str


class PinyinLookup(BaseModel):
    pinyinDict: Dict[str, Pinyin] = dict()

    @staticmethod
    def create() -> 'PinyinLookup':
        pinyinDict = PinyinLookup.construct()

        lines = FileUtils.loadFileAsList(FilePaths.pinyinList(), "Failed to load pinyin list")
        for line in lines:
            line = split(":", line)
            asc = line[0].strip().lower()
            hanyu = line[1].strip().lower()
            pinyinDict.pinyinDict.update({line[0].strip(): Pinyin.construct(ascii=asc,
                                                                            hanyu=hanyu,
                                                                            type=PinyinType.ASCII)})
            pinyinDict.pinyinDict.update({line[1].strip(): Pinyin.construct(ascii=asc,
                                                                            hanyu=hanyu,
                                                                            type=PinyinType.HANYU)})

        return pinyinDict

    def get(self, pinyin: str) -> Optional[Pinyin]:
        pinyin = pinyin.strip().lower()
        if len(self.pinyinDict) == 0:
            Utils.exitWithError("PinyinLookup is empty. Did you use create()?")

        pinyinObj = self.pinyinDict.get(pinyin)
        if not pinyinObj:
            return None

        return pinyinObj
