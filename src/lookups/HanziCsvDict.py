import csv
from typing import Dict, Optional

from pydantic.main import BaseModel

from src.commons import FilePaths
from src.lookups.PinyinLookup import PinyinLookup
from src.utils import Utils


class HanziData(BaseModel):
    hanzi: str
    concept: Optional[str] = None
    mnemonic: Optional[str] = None
    pinyin: Optional[str] = None


def create(pinyinLookup: PinyinLookup) -> Dict[str, HanziData]:
    hanziDict = {}

    with open(f"{FilePaths.uberHanziCsv()}", 'r') as file:
        reader = csv.reader(file, delimiter='\t')

        for row in reader:
            hanzi = row[1].strip()

            concept = row[2].split('<br>')[0].strip()

            mnemonic = ' '.join(row[3].split('<br><br>')[:-1]).strip()
            mnemonic = mnemonic.replace("<br>", "", 1)

            pinyin = convertAsciiPinyinToHanyu(row[4], pinyinLookup)

            data = HanziData(hanzi=hanzi, concept=concept, mnemonic=mnemonic, pinyin=pinyin)
            hanziDict.update({Utils.hashHanzi(hanzi): data})

    return hanziDict


def convertAsciiPinyinToHanyu(readings: str, pinyinLookup: PinyinLookup):
    hanyu = []
    for reading in readings.split("."):
        try:
            hanyu.append(pinyinLookup.get(reading).hanyu)
        except (Exception,):
            hanyu.append(reading)
    return '.'.join(hanyu)
