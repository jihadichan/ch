import json
import re
from re import split

from src.commons import FilePaths
from src.utils import FileUtils, Utils


def normalizePinyin(pinyin):
    return re.sub("ü", "v", pinyin)


def create():
    file = FileUtils.loadFileAsList(FilePaths.readingsMarkdownFile(), "Failed to load readings.md")
    obj = {}
    for line in file:
        if line.startswith("|") and not line.startswith("| Pinyin") and not line.startswith("| ---"):
            fragments = split("\\|", line)
            pinyin = normalizePinyin(fragments[1].strip())
            obj.update({pinyin: fragments[2].strip()})

    outputJson = f"var readingMnemonics = {json.dumps(obj)}"
    outputFile = FilePaths.outputDir().joinpath('readings.js')
    FileUtils.writeToFile(outputFile, outputJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")
