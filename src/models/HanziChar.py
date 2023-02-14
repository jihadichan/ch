from typing import List, Set, OrderedDict

from pydantic import BaseModel


class ExampleWord(BaseModel):
    cur: str
    trd: str
    mng: str
    pyn: str


class HanziChar(BaseModel):
    hnz: str
    cur: str
    trd: str
    isTrd: bool = False
    cmp: List[str] = list()
    mng: List[str] = list()
    pyn: List[str] = list()
    exm: List[ExampleWord] = list()

    @staticmethod
    def create(hanzi: str) -> 'HanziChar':
        return HanziChar.construct(hnz=hanzi)

    def addPinyin(self, candidate: str):
        candidate = candidate.strip().lower()
        if candidate not in self.pyn:
            self.pyn.append(candidate)
