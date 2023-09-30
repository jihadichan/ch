import csv
import json
import re

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

baseUrl = "https://resources.allsetlearning.com"

def fetchUrl(url) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch URL ({url}): {str(e)}")

def extractText(soup: BeautifulSoup):
    extracted_text = ""

    content_div = soup.find('div', {'id': 'mw-content-text'})
    if content_div is None:
        return ""

    for element in content_div.find_all(['p', 'div'], recursive=True):
        # Extract text from <p> elements
        if element.name == 'p':
            if element.get_text(strip=True) != "":
                extracted_text += "- " + element.get_text(strip=True) + "<br>"
        # Extract text from <li class="spaced"> elements
        elif element.name == 'div' and 'liju' in element.get('class', []) \
                and not element.find('ul', class_='dialog') \
                and not element.find('span', class_='expl'):
            li_elements = element.find_all('li', limit=3)  # Get the first 3 <li> elements
            for li in li_elements:
                classes = li.get('class', [])
                if 'x' in classes or 'o' in classes or 'q' in classes:
                    continue

                try:
                    example = ["", "", ""]

                    pinyin_text = li.find('span', class_='pinyin').get_text()
                    example[1] = pinyin_text

                    if li.find('span', class_='trans'):
                        trans_text = li.find('span', class_='trans').get_text()
                        example[2] = trans_text

                    li.find('span', class_='pinyin').decompose()
                    if li.find('span', class_='trans'):
                        li.find('span', class_='trans').decompose()
                    remaining_text = li.get_text(strip=True)
                    example[0] = remaining_text
                except Exception as e:
                    print(f"Failed at {li}")
                    # raise e
                    continue

                extracted_text += f"<ruby>{example[0]}<rt>{example[1]}</rt></ruby><br>{example[2]}<br>"
            extracted_text += "<hr><br>"


    return  re.sub(r'(<br>)+$', '', extracted_text.strip())

def main():
    chaptersUrls = [
        f"{baseUrl}/chinese/grammar/A1_grammar_points",
        f"{baseUrl}/chinese/grammar/A2_grammar_points",
        f"{baseUrl}/chinese/grammar/B1_grammar_points",
        f"{baseUrl}/chinese/grammar/B2_grammar_points",
    ]

    grammarPoints = {}
    rows = []

    for chapterUrl in chaptersUrls:
        soup = fetchUrl(chapterUrl)
        selected_elements = soup.select('tr:has(a[href^="/chinese/grammar"])')
        for element in selected_elements:
            a_tag = element.select_one('a[href^="/chinese/grammar"]')
            td_tags = element.select('td')

            href = a_tag['href']
            grammarPoints[href] = {
                "url": f"{baseUrl}{a_tag['href']}",
                "summary": a_tag.get_text(),
                "pattern": td_tags[1].get_text(strip=True) if len(td_tags) > 1 else None,
                "example": td_tags[2].get_text(strip=True) if len(td_tags) > 2 else None
            }

    for key, grammarPoint in grammarPoints.items():
        print(f"Fetching: {grammarPoint['url']}")
        soup = fetchUrl(grammarPoint["url"])

        notes = f"- {grammarPoint['summary']}<br>".replace('"', "'")
        notes += extractText(soup).replace('"', "'")
        rows.append([
            f"{grammarPoint['pattern']}<br>{grammarPoint['example']}".replace('"', "'"),  # sentence
            f"",                                                        # display
            notes,                                          # notes
            grammarPoint["url"],                                        # source
            "",                                                         # mp3
            "{}"                                                        # data
        ])

    with open("ubergrammar.csv", "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerows(rows)

if __name__ == "__main__":
    main()
