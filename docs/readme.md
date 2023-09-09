{:toc}

# Usage



## Generate hanzi helpers

Just run `make all`. For single commands see file.

- `hanzi_dict.zip` needs to imported as dictionary into Yomichan
- `mnemonics.js` belongs to the UberSentences deck
- `confs.js` belongs to the UberHanzi deck



## YomiChan custom audio URL server

Use `make server`. On Windows you probably needs to run the command directly:

```bash
python3 chcli.py yomichan --run-server
```



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



## Misc

- [Pinyin pronunciation](https://chinese.yabla.com/chinese-pinyin-chart.php), with mp3 files

- [Pinyin transliteration](https://mandarintools.com/pychart.html), `jue4 => juè`

- [Top10k hanzi](https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO)

- [Grammar guide](https://resources.allsetlearning.com/chinese/grammar/Grammar_points_by_level) (lots of examples but no sound)

  



## Decks

- [Grammar deck](https://ankiweb.net/shared/info/782551504) (6k notes, needs probably restructuring, no audio) 
- [Grammar deck](https://ankiweb.net/shared/info/797518833) (5k notes, has audio but uses Google Text-to-Speech, uses AllSet Learning grammar guide)
- [Grammar deck](https://ankiweb.net/shared/info/1549870487) (4k notes, has audio but sounds like the other)
- [Vocab decks](https://ankiweb.net/shared/decks/chinese%20vocab) (very little)
- [Beginner sentences](https://ankiweb.net/shared/info/1578796058) (451 notes)
- [Beginner vocab decks](https://ankiweb.net/shared/info/1322310186) (715 notes)



## Kindle Books

- Follow [this guide](https://www.cloudwards.net/remove-drm-from-kindle-books/) to install Calibre with DeDRM & KFXInput plugins.
- You might also need `pip install pycrypto` (see comments)
- Download the book from Amazon. Go to "Your Content and Devices", select the book, and then choose "Download & transfer via USB". You need `azw3` file. Importing the `kfx` file did not work. DRM wasn't removed.
- You probably need to convert to TXT instead of PDF, if Yomichan can't read the HTML.
  - If PDF, then convert via [CloudConvert](https://cloudconvert.com/pdf-to-html)
  - If TXT, then just drag into the browser
- Yomichan must have "Allow access to file URLs" enabled in the Chrome extension settings.



# Anki

## On Ubuntu 22.04

There are some problems with some thing called the Wayland protocol. You need some ENVs. Create a startup script.

```bash
#!/bin/bash

export QT_QPA_PLATFORM=xcb
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
anki
```



## Yomichan 

- For dictionaries `resources/` (from [Yomichan setup for Chinese](https://gist.github.com/shoui520/25460fd2e9fb194d3e5152fa2ce42ca2)). Simple import.

- For audio use the `chcli yomichan --run-server`. If it doesn't run then Yomichan inserts an empty field. Custom URL for audio source is:

  ```
  http://localhost:8888/get?word={term}&pinyin={reading}
  ```

- `TODO` Technically it should be possible to morph that KanjiDict into a Hanzi dict for character lookups



## AnkiConnect Settings

Settings to import from Yomichan pop-up to Anki. Settings > Anki > Configure Anki card format

- Deck: UberSentences_Vocab_1

- Model: UberSentences

- Settings

  ```
  sentence: {furigana}
  notes: {glossary}<br>Sentence:<br>{sentence}
  source: {clipboard-image}<br>{document-title}<br>{url}
  mp3: {audio}
  data: {}
  ```

  

## UberVocab

- Fields:

  ```
  sentence
  display
  notes
  sources
  mp3
  data
  ```

  
