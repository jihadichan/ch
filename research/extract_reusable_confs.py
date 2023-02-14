from pathlib import Path
from re import split

import click

"""
Extracts confs which the kanji exist in the top10k hanzi list. 
Also compares overlaps with kanji.
Run via `python3 extract_reusable_confs.py`
"""


def createHanziSet(path: Path, errorMessage: str) -> set:
    with open(path) as file:
        try:
            hanziSet = set()
            for line in file.readlines():
                line = split(";", line)
                hanziSet.update(line[1].strip())
            return hanziSet
        except Exception as e:
            exitWithException(errorMessage, e)


def createKanjiSet(path: Path, errorMessage: str) -> set:
    with open(path) as file:
        try:
            kanjiSet = set()
            for line in file.readlines():
                kanjiSet.update(line.strip())
            return kanjiSet
        except Exception as e:
            exitWithException(errorMessage, e)


def createConfList(path: Path, errorMessage: str) -> list:
    with open(path) as file:
        try:
            confList = []
            for line in file.readlines():
                confs = split(" cf ", line.strip())
                confList.append(confs)
            return confList
        except Exception as e:
            exitWithException(errorMessage, e)


def exitWithException(errorMessage: str, exception: Exception):
    click.secho(f"{exception}", fg="red")
    click.secho(f"{errorMessage}", fg="red")
    exit(1)


if __name__ == '__main__':
    hanziSet = createHanziSet(Path("../uberhanzi/resources/top10k_freq_list.csv"), "Failed to load hanzi file")
    kanjiSet = createKanjiSet(Path("files/all_kanji.txt"), "Failed to load freq list")
    confList = createConfList(Path("files/old_kanji_conf_list.txt"), "Failed to load conf list")

    # Check overlaps
    exists = 0
    for kanji in kanjiSet:
        if kanji in hanziSet:
            exists += 1

    reusableConfs = []
    for confs in confList:
        candidate = []
        for kanji in confs:
            if kanji in hanziSet:
                candidate.append(kanji)
        if len(candidate) > 1:
            reusableConfs.append(candidate)
            print(" cf ".join(candidate))

    print(f"Confs: {len(reusableConfs)}")

    click.secho(f"Hanzi list size: {len(hanziSet)}", fg="yellow")
    click.secho(f"Kanji list size: {len(kanjiSet)}", fg="yellow")
    click.secho(f"Matches: {exists}", fg="yellow")
    click.secho(f"No match: {len(kanjiSet) - exists}", fg="yellow")
