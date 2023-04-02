{:toc}

# UberHanzi



## Import

- Scrape new hanzi added to `uberhanzi/resources/hanzi_list.csv` (already scraped hanzi are in `uberhanzi/hanzi`)

  ```
  python3 chcli.py uberhanzi --scrape-hanzi
  ```

- Create the CSV for Anki

  ```
  python3 chcli.py uberhanzi --create-csv
  ```

  Best is to remove known hanzi from `uberhanzi/resources/hanzi_list.csv` (back the file up) and only create CSV with the new one so that you don't update the hanzi is your deck.



## Card format

```bash
id						 # uhz-HASHED_HANZI, e.g. uhz-c27c51f158
hanzi					 # text, e.g. 日										
concept					 # text, e.g. day, sun
mnemonic 				 # text, e.g. !done<br>日 - by day...	
playback 				 # readings for playback, e.g. にち.じつ
frequency				 # int, e.g. 123
searchkey				 # ｘ日
data					 # base64 encoded JSON
```



# Resources

- [Pinyin pronunciation](https://chinese.yabla.com/chinese-pinyin-chart.php), with mp3 files
- [Pinyin transliteration](https://mandarintools.com/pychart.html), `jue4 => juè`
- [Top10k hanzi](https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO)
- [Grammar guide](https://resources.allsetlearning.com/chinese/grammar/Grammar_points_by_level) (lots of examples but no sound)



# Decks

- [Grammar deck](https://ankiweb.net/shared/info/782551504) (6k notes, needs probably restructuring, no audio) 
- [Grammar deck](https://ankiweb.net/shared/info/797518833) (5k notes, has audio but uses Google Text-to-Speech, uses AllSet Learning grammar guide)
- [Grammar deck](https://ankiweb.net/shared/info/1549870487) (4k notes, has audio but sounds like the other)
- [Vocab decks](https://ankiweb.net/shared/decks/chinese%20vocab) (very little)
- [Beginner sentences](https://ankiweb.net/shared/info/1578796058) (451 notes)
- [Beginner vocab decks](https://ankiweb.net/shared/info/1322310186) (715 notes)



# Anki

## On Ubuntu 22.04

There are some problems with some thing called the Wayland protocol. You need some ENVs. Create a startup script.

```bash
#!/bin/bash

export QT_QPA_PLATFORM=xcb
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
anki
```



# Transition

## How to start

- Learn top3k hanzi
- Get Yomichan to work with Chinese
- Create Forvo mapper as local server
- Work through the [grammar guide](https://resources.allsetlearning.com/chinese/grammar/Grammar_points_by_level) and mine your first words
- Compliment with the [grammar deck](https://ankiweb.net/shared/info/797518833) maybe or go straight



## UberVocab

- [Yomichan setup for Chinese](https://gist.github.com/shoui520/25460fd2e9fb194d3e5152fa2ce42ca2) (needs Forvo mapper as local server)

## Yomichan Hanzi

- Technically it should be possible to morph that KanjiDict into a Hanzi dict. 

