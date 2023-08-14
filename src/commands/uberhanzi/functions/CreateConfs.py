import json

from pydantic import BaseModel
from typing import Optional, Dict

from src.lookups import HanziCsvDict
from src.lookups.HanziCsvDict import HanziData
from src.lookups.PinyinLookup import PinyinLookup
from src.commons import FilePaths
from src.utils import Utils, FileUtils


class HanziConf(BaseModel):
    hz: str
    meta: Optional[str] = None
    confs: set[str]
    mnemonic: Optional[str] = None


def create():
    pinyinLookup = PinyinLookup.create()
    hanziDict = HanziCsvDict.create(pinyinLookup)
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
                unicodeId = Utils.hanziToUnicode(hanzi)
                conf = confDict.get(unicodeId)
                if conf:
                    conf.confs.update(hanzis)
                else:
                    try:
                        hanziConf = HanziConf(hz=hanzi,
                                              meta=f"{hanzi} ({hanziData.pinyin}, {hanziData.concept})",
                                              confs=hanzis,
                                              mnemonic=hanziData.mnemonic)
                        confDict.update({unicodeId: hanziConf})
                    except Exception as e:
                        Utils.exitWithError(f"Can't find {hanzi} in known hanzi")
    return confDict
