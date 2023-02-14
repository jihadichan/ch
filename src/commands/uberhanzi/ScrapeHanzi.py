from src.commands.uberhanzi.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.PinyinLookup import PinyinLookup
from src.commands.uberhanzi.RadicalsLookup import RadicalsLookup
from src.commons import FilePaths, YablaClient
from src.models.HanziListChar import HanziListChar
from src.utils import FileUtils, Utils


def scrape(hanziFreqDict: HanziFreqLookup, pinyinLookup: PinyinLookup, radicalsLookup: RadicalsLookup):
    lines = FileUtils.loadFileAsList(FilePaths.hanziList(), "Failed to load hanzi list")

    charList = []
    for line in lines:
        charList.append(HanziListChar.fromHanziList(line))

    for hanziListChar in charList:
        Utils.printInfo(f"Checking {hanziListChar.hanzi}")
        hanziChar = YablaClient.lookUpHanzi(hanziListChar, hanziFreqDict, radicalsLookup)
        print(hanziChar)
        break

        # for each
        #   scrape the dictionary
        #   find hanzi entry
        #   scrape hanzi data
        #   download the mp3
        #   find all readings
        #   scrape example words
