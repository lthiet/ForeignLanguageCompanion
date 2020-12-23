import requests
from bs4 import BeautifulSoup

language = 'german'


def translate_word(word, specification=None):
    URL = f'https://dictionary.cambridge.org/dictionary/english-{language}/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

    soup = BeautifulSoup(page.content, 'html.parser')
    cats = soup.find_all(class_='dlink')
    l = []
    for c in cats:
        category = c.find_all(class_='dpos')[0].text

        defs = c.find_all(class_='ddef_d')
        for d in defs:
            definition = d.text
            translation = d.parent.parent.find_all(class_="dtrans")[0].text
            if category == specification or not specification in {'noun', 'adjective', 'verb'}:
                l.append((
                    f'{category} / {definition}',
                    translation
                ))
    return l
