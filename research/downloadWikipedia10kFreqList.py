
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

WIKI_URLS = [
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1-1000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/1001-2000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/2001-3000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/3001-4000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/4001-5000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/5001-6000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/6001-7000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/7001-8000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/8001-9000",
    "https://en.wiktionary.org/wiki/Appendix:Mandarin_Frequency_lists/9001-10000",
]
count = 1


def get_part_of_list(wiki_url):
    global count
    soup = BeautifulSoup(urlopen(wiki_url), "html.parser")
    words = soup.select("span.Hans")
    extracted = []

    for word in words:
        extracted.append({
            "freq": count,
            "word": word.text
        })
        count = count + 1

    return extracted


if __name__ == "__main__":
    freq_list = []

    for i, wiki_url in enumerate(WIKI_URLS):
        freq_list = freq_list + get_part_of_list(wiki_url)

    print(json.dumps(freq_list, ensure_ascii=False))
