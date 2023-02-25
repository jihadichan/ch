import glob
import re
from pathlib import Path

import requests

from src.commands.uberhanzi.lookups.PinyinLookup import PinyinLookup, PinyinType
from src.commons import FilePaths
from src.utils import Utils

baseUrl = "https://yabla.vo.llnwd.net/media.yabla.com/chinese_static/audio/alicia"


def scrape(pinyinLookup: PinyinLookup):
    mp3Dir = FilePaths.pinyinMp3Dir()
    knownMp3s = set()

    for file in glob.glob(f"{str(mp3Dir)}/*.mp3", recursive=True):
        file = Path(file)
        knownMp3s.add(re.sub("\\.mp3", "", file.name))

    for pinyin in pinyinLookup.pinyinDict.values():
        if pinyin.type == PinyinType.ASCII:

            if pinyin.ascii in knownMp3s:
                Utils.printInfo(f"'{pinyin.hanyu}' exists. Skipping...")
                continue

            Utils.printInfo(f"Downloading '{pinyin.hanyu}'...")
            outfile = mp3Dir.joinpath(f"{pinyin.ascii}.mp3")
            response = requests.get(f"{baseUrl}/{pinyin.ascii}.mp3", stream=True)
            with open(outfile, 'wb') as f:
                f.write(response.content)
