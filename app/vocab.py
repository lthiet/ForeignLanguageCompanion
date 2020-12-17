import pandas as pd
import requests
from bs4 import BeautifulSoup

# word_list = pd.read_csv("data/word_list.csv")
word = 'clean'
specification = 'verb'
language = 'german'

URL = f'https://dictionary.cambridge.org/dictionary/english-{language}/{word}'
page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(page.content, 'html.parser')
cats = soup.find_all(class_='dlink')
for c in cats:
    english_category = c.find_all(class_='dpos')[0].text

    defs = c.find_all(class_='ddef_d')
    for d in defs:
        english_definition = d.text
        translation = d.parent.parent.find_all(class_="dtrans")[0].text
        print(f'{english_category} / {english_definition}')
        print(translation)
