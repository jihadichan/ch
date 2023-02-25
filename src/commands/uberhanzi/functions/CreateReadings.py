import json
from re import split

from src.commons import FilePaths
from src.utils import FileUtils, Utils


def create():
    file = FileUtils.loadFileAsList(FilePaths.readingsMarkdownFile(), "Failed to load readings.md")
    obj = {}
    for line in file:
        if line.startswith("|") and not line.startswith("| Pinyin") and not line.startswith("| ---"):
            fragments = split("\\|", line)
            obj.update({fragments[1].strip(): fragments[2].strip()})

    outputJson = f"var readingMnemonics = {json.dumps(obj)}"
    outputFile = FilePaths.outputDir().joinpath('readings.js')
    FileUtils.writeToFile(outputFile, outputJson, f"Failed to write {outputFile}")
    Utils.printInfo(f"Wrote to {outputFile.absolute()}")
