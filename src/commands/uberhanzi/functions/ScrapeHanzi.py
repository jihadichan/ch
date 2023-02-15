import glob
import json
import re
from pathlib import Path

from src.commands.uberhanzi.lookups.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.lookups.RadicalsLookup import RadicalsLookup
from src.commons import FilePaths, YablaClient
from src.models.HanziListChar import HanziListChar
from src.utils import FileUtils, Utils


def scrape(hanziFreqDict: HanziFreqLookup, radicalsLookup: RadicalsLookup):
    hanziCharDirPath = FilePaths.hanziCharJsonDir()

    knownHanzi = set()
    for file in glob.glob(f"{str(hanziCharDirPath)}/*.json", recursive=True):
        file = Path(file)
        knownHanzi.add(re.sub("\\.json", "", file.name))

    lines = FileUtils.loadFileAsList(FilePaths.hanziList(), "Failed to load hanzi list")
    charList = []
    for line in lines:
        charList.append(HanziListChar.fromHanziList(line))

    for hanziListChar in charList:
        if hanziListChar.hanzi not in knownHanzi:
            Utils.printInfo(f"Scraping {hanziListChar.hanzi}...")
            hanziChar = YablaClient.lookUpHanzi(hanziListChar, hanziFreqDict, radicalsLookup)
            jsonString = json.dumps(hanziChar.dict(), ensure_ascii=False)
            outputFile = hanziCharDirPath.joinpath(f"{hanziListChar.hanzi}.json")
            FileUtils.writeToFile(outputFile, jsonString, f"Failed to write {outputFile}")
        else:
            Utils.printInfo(f"'{hanziListChar.hanzi}' already known, skipping...")
