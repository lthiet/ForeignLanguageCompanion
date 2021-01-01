import os
import requests
import json
from bs4 import BeautifulSoup
import string
from .config import cfg
from .lang import code_to_name
import re


def translate_cambridge(word, target=None, target_name=None):
    if target_name is None:
        target_url = code_to_name(target).lower()
    else:
        target_url = target_name

    URL = f'https://dictionary.cambridge.org/dictionary/english-{target_url}/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text.strip()
        parent = d.parent.parent.parent.parent.parent.parent
        category = parent.find_all(
            class_='dpos')
        while category == []:
            parent = parent.parent
            category = parent.find_all(
                class_='dpos')

        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            # TODO: deal with synonyms
            "word": translation.split(',')[0],
            "other": other
        })

    return l


def translate_de(word):
    def remove_determiner(text):
        # Der, Die, Das
        return text[3:]

    def noun_postprocess(entry):
        if entry['position'] in ['noun', 'noun_plural']:
            entry["word"] = remove_determiner(entry["word"])
        return entry

    return [noun_postprocess(e) for e in translate_cambridge(word, "de")]


def translate_tr(word):
    l = []
    n = 0
    done = False
    i = 1
    while not done:
        l += translate_cambridge(word + f'_{i}', 'tr')
        i += 1
        done = len(l) - n == 0
        n = len(l)
    return l


def remove_punctuation(s):
    r = ''
    for c in s:
        if not c in string.punctuation:
            r += c
    return r


def translate_azure(word, target):
    has_api = True
    try:
        # user has a API key, use this service instead
        key = cfg['translator']['key']
    except:
        # standard scraper method without API key
        has_api = False

    if not has_api:
        print("NO API KEY FOUND")
        return []

    key = cfg['translator']['key']
    location = cfg['translator']['location']
    url = f'https://api.cognitive.microsofttranslator.com/dictionary/lookup?api-version=3.0&from=en&to={target}'
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
    l = [
        {
            "position": e["posTag"],
            "word": e["normalizedTarget"],
            "other": str(e["confidence"]) + ': ' + ', '.join(a["normalizedText"] for a in e["backTranslations"])
        }
        for e in response["translations"]
    ]
    return l


def translate_word(word, target, specification=None):
    if target == 'de':
        return translate_de(word)
    elif target == 'tr':
        return translate_tr(word)
    elif target == 'zh-Hans':
        return translate_cambridge(word, target_name='chinese-simplified')
    elif target == 'pt':
        return translate_cambridge(word, target_name='portuguese')
    elif target == 'ms':
        return translate_cambridge(word, target_name='malaysian')
    elif target in ['ja', 'ko', 'ar', 'es', 'fr', 'id', 'it', 'pl', 'ca', 'cs', 'da', 'nb', 'ru', 'th', 'vi']:
        return translate_cambridge(word, target)
    # Last resort, try with Microsoft Translator API
    else:
        return translate_azure(word, target)
