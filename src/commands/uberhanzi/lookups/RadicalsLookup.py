from re import split
from typing import List, Optional, Any, Dict

from pydantic import BaseModel

from src.models.HanziListChar import HanziListChar
from src.commons import FilePaths
from src.utils import FileUtils, Utils


class RadicalsLookup(BaseModel):
    radicalsDict: Dict[str, HanziListChar] = dict()

    @staticmethod
    def create() -> 'RadicalsLookup':
        hanziFreqDict = RadicalsLookup.construct()
        radicalsFile = FilePaths.radicalsList()
        hanziList = FileUtils.loadFileAsList(radicalsFile, f"Failed to load {radicalsFile}")
        for line in hanziList:
            hanziListChar = HanziListChar.fromRadicalsList(line)
            hanziFreqDict.radicalsDict.update({hanziListChar.hanzi: hanziListChar})
        return hanziFreqDict

    def getMeaning(self, hanzi: str) -> str:
        hanzi = hanzi.strip().lower()
        if len(self.radicalsDict) == 0:
            Utils.exitWithError("HanziFreqDict is empty. Did you use create()?")

        char = self.radicalsDict.get(hanzi)
        if not char:
            return "Unknown"
        return char.meaning
