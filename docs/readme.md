{:toc}

# Transition





## UberVocab

- [Yomichan setup for Chinese](https://gist.github.com/shoui520/25460fd2e9fb194d3e5152fa2ce42ca2)



## UberHanzi

- You can get "character decomposition" from [here](https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=%E5%86%B5). See `_res/hanzi.html`.

- You can download the complete dictionary and they offer a parser in Pyhton: https://www.mdbg.net/chinese/dictionary?page=cedict

  But it's only words as it seems.

- Where to get frequency lists? Don't use Heisig order. 2000 most common then start to read.

- [This scraper](https://github.com/afzafri/Chinese-Pinyin-Dictionary-API) uses a nice dictionary, uses [this dictionary](https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=%E9%A5%BC)

  - MP3 directly in HTML. Quality is ok-ish
  - Results must be parsed to find the right result

- Can't you get all data from shared decks? => NO. Learn by frequency, not Heisig.

  - [Heisig Simplified Chinese](https://ankiweb.net/shared/info/1984285834), 3018 notes, good audio
  - [Most Common 3000 Chinese Hanzi Characters](https://ankiweb.net/shared/info/39888802), ok-ish audio



### Plan

- Get list of 2000 top hanzi, better like top 8000 and then suspends the rest
- Create CLI in Python, not Java (because types)
- Create similar output to UberKanji
- ~~Add "character decomposition" as iframe (works), no need for~~ Just iframe the whole page like jisho
- Download MP3 from the dictionary
- Limit to 10 example words, select based on different pinyin. First check all pinyin, add different ones, then fill up
- Make CLI that the list is easily extensible, but without Google Wavenet
- ~~Add radicals additionally (see [here](https://ankiweb.net/shared/info/842457706)), they all have pinyin + meaning.~~ Radicals don't matter, make up your own