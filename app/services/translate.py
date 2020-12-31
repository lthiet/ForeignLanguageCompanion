import os
import requests
import json
from bs4 import BeautifulSoup
import string
from .config import cfg
from .lang import code_to_name
import re


def language_specific_processing(entry, lang=None):
    if lang == 'de':
        if entry['position'] == 'NOUN' or entry['position'] == 'OTHER':
            entry["word"] = entry["word"][0].upper() + entry["word"][1:]
            return entry
        else:
            return entry
    else:
        return entry


def translate_de(word):
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
            translation = d.parent.parent.find_all(class_="dtrans")[
                0].text
            if category == 'noun' or category == 'noun plural':
                translation = translation.split(' ')[1]

            l.append({
                "position": category,
                "word": translation,
                "other": definition
            })
    return l


def translate_tr(word):
    URL = f'https://dictionary.cambridge.org/dictionary/english-turkish/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text
        translation = re.split('，|；', translation)[0]
        category = d.parent.parent.parent.parent.parent.parent.find_all(
            class_='dpos')
        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            "word": translation,
            "other": other
        })

    return l


def translate_ja(word):
    URL = f'https://dictionary.cambridge.org/dictionary/english-japanese/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text
        translation = re.split('，|；', translation)[0]
        category = d.parent.parent.parent.parent.parent.parent.find_all(
            class_='dpos')
        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            "word": translation,
            "other": other
        })

    return l


def translate_ko(word):
    URL = f'https://dictionary.cambridge.org/dictionary/english-korean/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text
        translation = re.split('，|；', translation)[0]
        category = d.parent.parent.parent.parent.parent.parent.find_all(
            class_='dpos')
        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            "word": translation,
            "other": other
        })

    return l


def translate_zh(word):
    URL = f'https://dictionary.cambridge.org/dictionary/english-chinese-traditional/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text
        translation = re.split('，|；', translation)[0]
        category = d.parent.parent.parent.parent.parent.parent.find_all(
            class_='dpos')
        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            "word": translation,
            "other": other
        })

    return l


def remove_punctuation(s):
    r = ''
    for c in s:
        if not c in string.punctuation:
            r += c
    return r


def translate_es(word):
    URL = f'https://dictionary.cambridge.org/dictionary/english-spanish/{word}'
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, 'html.parser')
    defs = soup.find_all(class_='ddef_d')
    l = []
    for d in defs:
        other = d.text
        translation = d.parent.parent.find_all(class_='dtrans')[0].text
        translation = re.split('，|；', translation)[0]
        category = d.parent.parent.parent.parent.parent.parent.find_all(
            class_='dpos')
        category = category[0].text if category != [] else ''
        l.append({
            "position": category,
            "word": translation,
            "other": other
        })

    return l


def supported_Lang_translate(word, target):
    if target == 'de':
        return translate_de(word)
    elif target == 'tr':
        return translate_tr(word)
    elif target == 'es':
        return translate_es(word)
    elif target == 'zh-Hans':
        return translate_zh(word)
    elif target == 'ja':
        return translate_ja(word)
    elif target == 'ko':
        return translate_ko(word)


def translate_word(word, target, specification=None):
    has_api = True
    try:
        # user has a API key, use this service instead
        key = cfg['translator']['key']
    except:
        # standard scraper method without API key
        has_api = False

    supported_lang = target in [
        'de',
        'tr',
        'es',
        'zh-Hans',
        'ja',
        'ko'
    ]

    if supported_lang:
        return supported_Lang_translate(word, target)
    elif has_api:
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
        l = [language_specific_processing({
            "position": e["posTag"],
            "word": e["displayTarget"],
            "other": "confidence : " + str(e["confidence"])}, lang=target)
            for e in response["translations"]]
        return l
    else:
        return []
