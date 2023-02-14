from re import split
from typing import List

from pydantic import BaseModel

from src.utils import Utils


class HanziListChar(BaseModel):
    """
    Maps entries from the hanzi list and frequency list to make lookups with
    """

    hanzi: str
    freq: int
    readings: List[str]
    meaning: str

    @staticmethod
    def fromTop10kFreqList(line: str) -> 'HanziListChar':
        lineSplit = split(";", line.strip())
        if len(lineSplit) < 5 or not lineSplit[0].isnumeric():
            Utils.exitWithError(f"Malformed line: '{line.strip()}', must look like '9933;鴒;1;100;ling2'")

        meaning = "Unknown"
        if len(lineSplit) == 6:
            meaning = lineSplit[5]

        return HanziListChar.construct(hanzi=lineSplit[1].strip(),
                                       freq=int(lineSplit[0].strip()),
                                       readings=split("/", lineSplit[4]),
                                       meaning=meaning)

    @staticmethod
    def fromRadicalsList(line: str) -> 'HanziListChar':
        lineSplit = split(";", line.strip())
        if len(lineSplit) != 2:
            Utils.exitWithError(f"Malformed line: '{line.strip()}', must look like '几;table'")

        return HanziListChar.construct(hanzi=lineSplit[0].strip(),
                                       meaning=lineSplit[1].strip().lower())

    @staticmethod
    def fromHanziList(line: str) -> 'HanziListChar':
        lineSplit = split(";", line.strip())
        if len(lineSplit) != 3 or not lineSplit[1].isnumeric():
            Utils.exitWithError(f"Malformed line: '{line.strip()}', must look like '的;1;de,di2,di4'")

        return HanziListChar.construct(hanzi=lineSplit[0].strip(),
                                       freq=lineSplit[1].strip(),
                                       readings=split("/", lineSplit[2]))
