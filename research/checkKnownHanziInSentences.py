
sentencesList = []
knownHanziDict = set()
usedHanziSet = set()
knownHanziSet = set()
unknownHanziSet = set()

with open("files/learnedHanzi.txt", 'r') as file:
    learnedHanzi = file.readlines()

    for hanzi in learnedHanzi:
        knownHanziDict.add(hanzi.strip())

with open('files/allset_sentences.txt', 'r') as file:
    for line in file:
        sentencesList.append(line.strip())


for sentence in sentencesList:
    for char in sentence:
        usedHanziSet.add(char)
        if char in knownHanziDict:
            knownHanziSet.add(char)
        else:
            unknownHanziSet.add(char)


totalSentences = len(sentencesList)
print(f"Total sentences : {totalSentences}")
print(f"Total hanzi     : {len(usedHanziSet)}")
print(f"Known hanzi     : {len(knownHanziSet)}")
print(f"Unknown hanzi   : {len(unknownHanziSet)}")
for hanzi in unknownHanziSet:
    print(hanzi)
