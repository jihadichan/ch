import base64
import glob
import hashlib
import json
import re
from pathlib import Path

from src.commands.uberhanzi.lookups.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.lookups.PinyinLookup import PinyinLookup
from src.commands.uberhanzi.lookups.RadicalsLookup import RadicalsLookup
from src.commons import FilePaths, YablaClient
from src.models.HanziChar import HanziChar
from src.models.HanziListChar import HanziListChar
from src.utils import FileUtils, Utils


def create(hanziFreqDict: HanziFreqLookup, radicalsLookup: RadicalsLookup, pinyinLookup: PinyinLookup):

    # for key, hanziListChar in hanziFreqDict.freqDict.items():
    #     for reading in hanziListChar.readings:
    #         if not re.search("\\d", reading) and reading != "":
    #             print(f"{hanziListChar.freq}:{reading}")
    # exit()

    lines = FileUtils.loadFileAsList(FilePaths.hanziList(), "Failed to load hanzi list")
    characters = []
    for line in lines:
        characters.append(HanziListChar.fromHanziList(line))

    rows = ""
    for hanziListChar in characters:
        jsonString = loadHanziCharAsJsonString(hanziListChar)
        hanziChar = HanziChar.parse_obj(json.loads(jsonString))

        row = [
            getID(hanziListChar),                                   # ID
            hanziListChar.hanzi,                                    # hanzi
            "",                                                     # concept
            "",                                                     # mnemonic
            getPinyin(hanziChar, pinyinLookup),                     # playback
            str(hanziFreqDict.getFreq(hanziListChar.hanzi)),        # frequency
            f"ｘ{hanziListChar.hanzi}",                             # search field
            str(base64.b64encode(jsonString.encode()).decode())     # json data
        ]
        rows += "\t".join(row)
        rows += "\n"

    outputFile = FilePaths.outputDir().joinpath('uberhanzi.csv')
    FileUtils.writeToFile(outputFile, rows, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")


def getID(hanziListChar: HanziListChar) -> str:
    return f"uhz-{hashlib.shake_256(hanziListChar.hanzi.encode()).hexdigest(3)}"


def loadHanziCharAsJsonString(hanziListChar: HanziListChar) -> str:
    jsonFilePath = FilePaths.hanziCharJsonDir().joinpath(f"{hanziListChar.hanzi}.json")
    return FileUtils.loadFileAsString(jsonFilePath, f"Failed to load {jsonFilePath}")


def getPinyin(hanziChar: HanziChar, pinyinLookup: PinyinLookup) -> str:
    playback = []
    for pinyin in hanziChar.pyn:
        playback.append(pinyinLookup.get(pinyin).ascii)
    return ".".join(playback)
