import json

from src.commons import FilePaths
from src.lookups import HanziCsvDict
from src.lookups.PinyinLookup import PinyinLookup
from src.utils import Utils, FileUtils


def run(pinyinLookup: PinyinLookup):
    hanziCsvDict = HanziCsvDict.create(pinyinLookup)
    mnemonicsDict = {}
    for key, hanzi in hanziCsvDict.items():
        if '- <br>' in hanzi.mnemonic:  # if the hanzi has no mnemonic text then it's safe to assume that the card is untouched
            continue
        mnemonicsDict.update({Utils.hanziToUnicode(hanzi.hanzi): {
            "kj": hanzi.hanzi,
            "m": hanzi.mnemonic,
            "r": hanzi.pinyin,
            "rtk": "",
            "cp": hanzi.concept
        }})

    outputJson = f"var mnemonicsMap = {json.dumps(mnemonicsDict, ensure_ascii=False)}"
    outputFile = FilePaths.outputDir().joinpath('mnemonics.js')  # Must have this name
    FileUtils.writeToFile(outputFile, outputJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")
