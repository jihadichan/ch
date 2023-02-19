import base64
import hashlib
import json
from re import split

from src.commands.uberhanzi.lookups.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.lookups.PinyinLookup import PinyinLookup
from src.commons import FilePaths
from src.models.HanziChar import HanziChar
from src.models.HanziListChar import HanziListChar
from src.utils import FileUtils, Utils


def create(hanziFreqDict: HanziFreqLookup, pinyinLookup: PinyinLookup):
    lines = FileUtils.loadFileAsList(FilePaths.hanziList(), "Failed to load hanzi list")
    characters = []
    for line in lines:
        characters.append(HanziListChar.fromHanziList(line))

    rows = ""
    for hanziListChar in characters:
        jsonString = loadHanziCharAsJsonString(hanziListChar)
        try:
            hanziChar = HanziChar.parse_obj(json.loads(jsonString))
        except (Exception,):
            Utils.printInfo(f"Failed to map JSON for '{hanziListChar.hanzi}'. Probably insufficient data, see https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define={hanziListChar.hanzi}")
            continue

        row = [
            getID(hanziListChar),                                # ID
            hanziListChar.hanzi,                                 # hanzi
            createConcept(hanziChar),                            # concept
            createMnemonics(hanziListChar, hanziChar),           # mnemonic
            getPinyin(hanziChar, pinyinLookup),                  # playback
            str(hanziFreqDict.getFreq(hanziListChar.hanzi)),     # frequency
            f"ｘ{hanziListChar.hanzi}",                          # search field
            str(base64.b64encode(jsonString.encode()).decode())  # json data
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
        pyn = pinyinLookup.get(pinyin, hanziChar)
        if pyn:
            playback.append(pyn.ascii)
    return ".".join(playback)


def createMnemonics(hanziListChar: HanziListChar, hanziChar: HanziChar):
    pyn = hanziChar.pyn[0]

    html = "<br>"
    html += f"{hanziListChar.hanzi} - <br>"
    html += f"{pyn} - <br>"
    html += f"<br><br>"
    html += f"---<br>"

    exm = hanziChar.exm[0]
    for candidate in hanziChar.exm:
        if len(candidate.cur) > 1 and pyn in candidate.pyn:
            exm = candidate
            break

    if hanziChar.isTrd:
        html += f"<ruby>{exm.trd}<rt>{exm.pyn}</rt></ruby> ({pyn}, trdFrm of {exm.cur}, {exm.mng})"
    else:
        html += f"<ruby>{exm.cur}<rt>{exm.pyn}</rt></ruby> ({pyn}, {exm.mng})"

    return html


def createConcept(hanziChar: HanziChar):
    combinedMeanings = ", ".join(hanziChar.mng)
    meanings = split(",", combinedMeanings)
    main = meanings.pop(0).strip()
    sliced = meanings[0:3]
    for index, term in enumerate(sliced):
        sliced[index] = sliced[index].strip()

    html = main
    if len(sliced) > 1:
        html += "<br>("
        html += ", ".join(sliced)
        html += ")"
    elif len(sliced) > 0:
        html += f", {sliced[0]}"

    return html
