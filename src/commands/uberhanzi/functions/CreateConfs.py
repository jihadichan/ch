import csv
import json

from pydantic import BaseModel
from typing import Optional, Dict

from src.commands.uberhanzi.lookups.PinyinLookup import PinyinLookup
from src.commons import FilePaths
from src.utils import Utils, FileUtils


class HanziData(BaseModel):
    hanzi: str
    concept: Optional[str] = None
    mnemonic: Optional[str] = None
    pinyin: Optional[str] = None


class HanziConf(BaseModel):
    hz: str
    meta: Optional[str] = None
    confs: set[str]
    mnemonic: Optional[str] = None


def create():
    pinyinLookup = PinyinLookup.create()
    hanziDict = createHanziDict(pinyinLookup)
    confDict = createConfDict(hanziDict)
    dict_of_dicts = {key: {**conf.dict(), 'confs': list(conf.confs)} for key, conf in confDict.items()}

    outputJson = f"var confMap = {json.dumps(dict_of_dicts, ensure_ascii=False)}"
    outputFile = FilePaths.outputDir().joinpath('confs.js')
    FileUtils.writeToFile(outputFile, outputJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")


def createConfDict(hanziDict: Dict[str, HanziData]) -> Dict[str, HanziConf]:
    confDict = {}
    with open(f"{FilePaths.confFile()}", 'r') as file:
        for line in file:
            hanzis = line.strip().split(" cf ")
            for hanzi in hanzis:
                hanziData = hanziDict.get(Utils.hashHanzi(hanzi))
                hanziConf = HanziConf(hz=hanzi,
                                      meta=f"{hanzi} ({hanziData.pinyin}, {hanziData.concept})",
                                      confs=hanzis,
                                      mnemonic=hanziData.mnemonic)
                confDict.update({Utils.hanziToUnicode(hanzi): hanziConf})
    return confDict


def createHanziDict(pinyinLookup: PinyinLookup) -> Dict[str, HanziData]:
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
