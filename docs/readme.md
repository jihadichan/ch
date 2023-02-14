{:toc}

# Resources

- [Pinyin pronunciation](https://chinese.yabla.com/chinese-pinyin-chart.php), with mp3 files
- [Pinyin transliteration](https://mandarintools.com/pychart.html), `jue4:juè`



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



### To-Do's

- [x] Get list of 2000 top hanzi, better like top 8000 and then suspends the rest

- [x] Create CLI in Python, not Java (because types)

- [ ] Create similar output to UberKanji

- [ ]  ~~Add "character decomposition" as iframe (works), no need for~~ Just iframe the whole page like jisho

- [x]  Download MP3 from the dictionary

- [x]  Determine what the most common reading is

- [x]  ~~Add radicals to hanzi list, freq=99999~~

- [x]  Limit to 10 example words, select based on different pinyin. First check all pinyin, add different ones, then fill up with those which come first

- [x]  Make CLI that the list is easily extensible, but without Google Wavenet

- [ ] UberKanji CSV rows look like this:

  ```bash
  国                           # kanji (first column must be ID)
  3                           # ID (should be unique string)																
  こく.くに					  # reading for playback
  3							# frequency, make 99999 if not known
  624							# RTK index, remove
  multireading				# tags, remove
  "searchKey": "ｘ国"		   # add as field
  %7B%22meanings%22%3A%22		# URL-encoded JSON, see below 
  ```

- [ ]  UberKanji JSON:

  ```json
  {
  	"meanings": "country",
  	"frequency": 3,
  	"components": "囗:+box+or+enclosure+radical+(no.+31);+box<br>玉:+jewel;+ball",
  	"strokes": 8,
  	"rtkKeyword": "country",
  	"rtkIndex": 624,
  	"onReadings": "コク",
  	"kunReadings": "くに",
  	"wordExamples": [{
  		"word": "国",
  		"reading": "くに",
  		"meanings": "country,+state+(Noun)<br>region<br>national+government,+central+government<br>home+(i.e.+hometown,+home+country)<br>province+(of+Japan)<br>land,+earth",
  		"score": 1,
  		"usuallyWrittenAs": "Kanji",
  		"freqNF": "466",
  		"freqWK": "36",
  		"foundKanjiReading": "くに",
  		"type": "fnKJ"
  	}, {
  		"word": "国々",
  		"reading": "くにぐに",
  		"meanings": "countries+(Noun)",
  		"score": 1,
  		"usuallyWrittenAs": "Kanji",
  		"freqWK": "5777",
  		"foundKanjiReading": "くに",
  		"type": "oFrm"
  	}],
  	"mostCommonReadings": {
  		"コク": 73,
  		"くに": 5
  	},
  	"scoredReadings": {
  		"コク": {
  			"score": 65,
  			"fbKJ": 65,
  			"fbKN": 0
  		},
  		"くに": {
  			"score": 4,
  			"fbKJ": 4,
  			"fbKN": 0
  		}
  	},
  	"compoundReading": "こく.くに",
  	"searchKey": "ｘ国"
  }
  ```

- [ ]  Shorten to:

  ```json
  {
  	"meanings": "country",
  	"wordExamples": [{
  		"word": "国",
  		"reading": "くに",
  		"meanings": "country,+state+(Noun)<br>region<br>national+government,+central+government<br>home+(i.e.+hometown,+home+country)<br>province+(of+Japan)<br>land,+earth",
  	}, {
  		"word": "国々",
  		"reading": "くにぐに",
  		"meanings": "countries+(Noun)"
  	}],
  	"searchKey": "ｘ国"
  }
  ```
  
  # Dictionary scraping
  
  - [ ] Some hanzi which have multiple readings have also multiple entries, see 的. 
  - [ ] Some hanzi are "traditional". Left side shows the contemporary form, see 韆. Maybe create special marker?