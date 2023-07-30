from src.lookups import HanziCsvDict
from src.lookups.PinyinLookup import PinyinLookup


def run(pinyinLookup: PinyinLookup):
    hanziCsvDict = HanziCsvDict.create(pinyinLookup)
    for key, hanzi in hanziCsvDict.items():
        print(hanzi)
