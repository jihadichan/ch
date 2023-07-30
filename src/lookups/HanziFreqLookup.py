from typing import Dict

from pydantic import BaseModel

from src.models.HanziListChar import HanziListChar
from src.commons import FilePaths
from src.utils import FileUtils, Utils


class HanziFreqLookup(BaseModel):
    freqDict: Dict[str, HanziListChar] = dict()

    @staticmethod
    def create() -> 'HanziFreqLookup':
        hanziFreqDict = HanziFreqLookup.construct()
        top10kFile = FilePaths.top10kHanziFreqList()
        hanziList = FileUtils.loadFileAsList(top10kFile, f"Failed to load {top10kFile}")
        for line in hanziList:
            hanziListChar = HanziListChar.fromTop10kFreqList(line)
            hanziFreqDict.freqDict.update({hanziListChar.hanzi: hanziListChar})
        return hanziFreqDict

    def getFreq(self, hanzi: str) -> int:
        hanzi = hanzi.strip().lower()
        if len(self.freqDict) == 0:
            Utils.exitWithError("HanziFreqDict is empty. Did you use create()?")

        char = self.freqDict.get(hanzi)
        if not char:
            return 99999
        return char.freq

    def getMeaning(self, hanzi: str) -> str:
        hanzi = hanzi.strip()
        if len(self.freqDict) == 0:
            Utils.exitWithError("HanziFreqDict is empty. Did you use create()?")

        char = self.freqDict.get(hanzi)
        if not char:
            return "Unknown"
        return char.meaning
