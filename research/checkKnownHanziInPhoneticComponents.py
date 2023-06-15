import json

maxWords = 10000
maxKnownHanzi = 2000
phoneticComponents = []
knownHanziSet = set()
unusedHanzi = set()
missingHanziSet = set()
knownWords = 0
unknownWords = 0

with open("files/top10kHanziList.txt", 'r') as file:
    top10kHanzi = file.readlines()

    for hanzi in top10kHanzi[:maxKnownHanzi]:
        knownHanziSet.add(hanzi.strip())
        unusedHanzi.add(hanzi.strip())

with open('files/phoneticCompounds.json', 'r') as file:
    components = json.load(file)[:maxWords]

    for hanzi in components:
        phoneticComponents.append(hanzi.strip())


for word in phoneticComponents:
    allHanziAreKnown = True
    for char in word:
        if char not in knownHanziSet:
            missingHanziSet.add(char)
            allHanziAreKnown = False
        else:
            unusedHanzi.discard(char)

    if allHanziAreKnown:
        knownWords = knownWords + 1
    else:
        unknownWords = unknownWords + 1
        print(word)


totalComponents = len(phoneticComponents)
print(f"Total components   : {totalComponents}")
print(f"Known hanzi        : {len(knownHanziSet)}")
print(f"Readable components: {knownWords} ({round(knownWords / totalComponents * 100, 2)}%)")
print(f"Missing components : {unknownWords} ({round(unknownWords / totalComponents * 100, 2)}%)")

print(json.dumps(list(missingHanziSet), ensure_ascii=False))
