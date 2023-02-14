import json
import re
from collections import Counter
from re import split

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from src.commands.uberhanzi.HanziFreqLookup import HanziFreqLookup
from src.commands.uberhanzi.PinyinLookup import PinyinLookup
from src.commands.uberhanzi.RadicalsLookup import RadicalsLookup
from src.models.HanziChar import HanziChar, ExampleWord
from src.models.HanziListChar import HanziListChar
from src.utils import Utils

yablaBaseUrl = "https://chinese.yabla.com/chinese-english-pinyin-dictionary.php"
mdbgBaseUrl = "https://www.mdbg.net/chinese/dictionary-ajax?c=cdcd"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


class YablaWord(BaseModel):
    currentForm: str = None
    traditionalForm: str = None
    pinyin: str = None
    meaning: str = None


def lookUpHanzi(hanziListChar: HanziListChar, hanziFreqDict: HanziFreqLookup, radicalsLookup: RadicalsLookup) -> HanziChar:
    url = f"{yablaBaseUrl}?define={hanziListChar.hanzi}"
    response = requests.get(url, headers=headers)

    if len(hanziListChar.hanzi) != 1:
        Utils.exitWithError(f"Desired query to look up hanzi must be one single character, got '{hanziListChar.hanzi}'")
    if response.status_code != 200:
        Utils.exitWithError(f"URL returned unexpected code: '{response.status_code}', need 200. URL: {url}")
    if "No matches found for" in response.text:
        Utils.exitWithError(f"No results for {hanziListChar.hanzi}, check {url}")

    yablaWords = []
    dom = BeautifulSoup(response.text, 'html.parser')
    for entryElem in dom.find_all(class_="entry"):  # every entry is a word (or single hanzi))

        yablaWord = YablaWord.construct()
        for wordElem in entryElem.find_all(class_="word"):
            word = wordElem.text.strip()
            if "Trad." in word:
                yablaWord.traditionalForm = re.sub(r"Trad\.\s?", "", word, re.IGNORECASE).strip()
            else:
                yablaWord.currentForm = word

        pinyin = entryElem.find(class_="pinyin")
        yablaWord.pinyin = pinyin.text.strip()

        meaning = entryElem.find(class_="meaning")
        meaning = meaning.text
        meaning = split('\\n', meaning)
        for index, m in enumerate(meaning):
            if "CL:" in m:
                meaning.pop(index)
        yablaWord.meaning = ', '.join(meaning)

        yablaWords.append(yablaWord)

    hanziChar = HanziChar.create(hanzi=hanziListChar.hanzi)

    # check if traditional form
    for yablaWord in yablaWords:
        if yablaWord.traditionalForm and yablaWord.traditionalForm == hanziListChar.hanzi:
            hanziChar.isTrd = True

    # identify hanzi
    scoredReadings = {}
    wordExamples = []
    for index, yablaWord in enumerate(yablaWords):
        if yablaWord.currentForm == hanziListChar.hanzi or yablaWord.traditionalForm == hanziListChar.hanzi:
            hanziChar.trd = yablaWord.traditionalForm
            hanziChar.cur = yablaWord.currentForm
            hanziChar.mng.append(yablaWord.meaning)
            hanziChar.addPinyin(yablaWord.pinyin)
            scoredReadings.update({yablaWord.pinyin: 0})
        else:
            wordExamples.append(yablaWord)

    # score readings
    for reading in scoredReadings.keys():
        score = 0
        for yablaWord in yablaWords:
            if reading in yablaWord.pinyin:
                score += 1
        scoredReadings[reading] = score

    hanziChar.pyn.clear()
    counter = Counter(scoredReadings)
    for obj in counter.most_common():
        hanziChar.addPinyin(obj[0])

    # find at least one example for each reading
    for pinyin in hanziChar.pyn:
        for index, yablaWord in enumerate(wordExamples):
            if pinyin in yablaWord.pinyin:
                hanziChar.exm.append(ExampleWord.construct(cur=yablaWord.currentForm,
                                                           trd=yablaWord.traditionalForm,
                                                           mng=yablaWord.meaning,
                                                           pyn=yablaWord.pinyin))
                wordExamples.pop(index)
                break

    # fill up with other words
    for yablaWord in wordExamples:
        exampleWord = ExampleWord.construct(cur=yablaWord.currentForm,
                                            trd=yablaWord.traditionalForm,
                                            mng=yablaWord.meaning,
                                            pyn=yablaWord.pinyin)
        hanziChar.exm.append(exampleWord)
        if len(hanziChar.exm) == 10:
            break

    # get radical compounds
    url = f"{mdbgBaseUrl}&i={hanziListChar.hanzi}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        Utils.exitWithError(f"URL returned unexpected code: '{response.status_code}', need 200. URL: {url}")

    if "No results found" not in response.text:
        dom = BeautifulSoup(response.text, 'html.parser')
        for link in dom.find_all("a"):
            component = link.text.strip()
            if hanziListChar.hanzi not in link.text:
                meaning = hanziFreqDict.getMeaning(component)
                if "Unknown" in meaning:
                    meaning = radicalsLookup.getMeaning(component)
                hanziChar.cmp.append(f"{component} ({meaning})")

    return hanziChar
