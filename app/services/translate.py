import os
import requests
import json
from bs4 import BeautifulSoup
from .config import cfg
lang = 'de'


def language_specific_processing(entry, lang=None):
    if lang == 'de':
        if entry['position'] == 'NOUN':
            entry["word"] = entry["word"][0].upper() + entry["word"][1:]
            return entry
    else:
        return entry


def translate_word(word, specification=None):
    has_api = True
    try:
        # user has a API key, use this service instead
        key = cfg['translator']['key']
    except:
        # standard scraper method without API key
        has_api = False

    if has_api:
        key = cfg['translator']['key']
        location = cfg['translator']['location']
        url = f'https://api.cognitive.microsofttranslator.com/dictionary/lookup?api-version=3.0&from=en&to={lang}'
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
        }
        body = {
            'text': word
        }
        response = requests.post(url, headers=headers, json=body)
        response = json.loads(response.content.decode())
        l = [language_specific_processing({
            "position": e["posTag"],
            "word": e["displayTarget"],
            "other": "confidence : " + str(e["confidence"])}, lang=lang)
            for e in response["translations"]]
        return l
    else:
        URL = f'https://dictionary.cambridge.org/dictionary/english-german/{word}'
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
                if category == 'noun' or category == 'noun plural':
                    translation = translation.split(' ')[1]

                if category == specification or not specification in {'noun', 'adjective', 'verb'}:
                    l.append({
                        "position": category,
                        "word": translation,
                        "other": definition
                    })
        return l
