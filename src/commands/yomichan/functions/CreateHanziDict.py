import json

from src.commons import FilePaths
from src.lookups import HanziCsvDict
from src.lookups.PinyinLookup import PinyinLookup
from src.utils import FileUtils, Utils


def run(pinyinLookup: PinyinLookup):
    hanziCsvDict = HanziCsvDict.create(pinyinLookup)
    hanziList = []
    for key, hanzi in hanziCsvDict.items():

        mnemonicLines = [hanzi.concept, ""]
        for line in hanzi.mnemonic.split("<br>"):
            mnemonicLines.append(line)
        mnemonicLines.append("")
        mnemonicLines.append(hanzi.pinyin)

        hanziList.append([
            hanzi.hanzi,
            "",
            "",
            "",
            mnemonicLines,
            {}
        ])

    outputJson = json.dumps(hanziList, ensure_ascii=False)
    outputFile = FilePaths.outputDir().joinpath('kanji_bank_1.json')  # Must have this name
    FileUtils.writeToFile(outputFile, outputJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")

    indexJson = '{"title":"HANZIDIC (English)","format":3,"revision":"hanzidic2","sequenced":false}'
    outputFile = FilePaths.outputDir().joinpath('index.json')
    FileUtils.writeToFile(outputFile, indexJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")
