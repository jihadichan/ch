import json

maxWords = 10000
maxKnownHanzi = 2000
top10kWordsList = []
knownHanziDict = set()
unusedHanzi = set()
missingHanziSet = set()
knownWords = 0
unknownWords = 0

with open("files/top10kHanziList.txt", 'r') as file:
    top10kHanzi = file.readlines()

    for hanzi in top10kHanzi[:maxKnownHanzi]:
        knownHanziDict.add(hanzi.strip())
        unusedHanzi.add(hanzi.strip())

with open('files/wikipediaTop10kFreqList.json', 'r') as file:
    tuples = json.load(file)[:maxWords]

    for obj in tuples:
        top10kWordsList.append(obj['word'].strip())


for word in top10kWordsList:
    allHanziAreKnown = True
    for char in word:
        if char not in knownHanziDict:
            missingHanziSet.add(char)
            allHanziAreKnown = False
        else:
            unusedHanzi.discard(char)

    if allHanziAreKnown:
        knownWords = knownWords + 1
    else:
        unknownWords = unknownWords + 1
        print(word)


totalWords = len(top10kWordsList)
print(f"Total words     : {totalWords}")
print(f"Known hanzi     : {len(knownHanziDict)}")
print(f"Readable Words  : {knownWords} ({round(knownWords / totalWords * 100, 2)}%)")
print(f"Unreadable Words: {unknownWords} ({round(unknownWords / totalWords * 100, 2)}%)")
print(f"Missing hanzi   : {len(missingHanziSet)}")
print(f"Unused hanzi    : {len(unusedHanzi)}")
