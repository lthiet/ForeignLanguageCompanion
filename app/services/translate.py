import os
from flask.globals import request
import requests
import json
from bs4 import BeautifulSoup
import string
from app.services.config import cfg, get_header
from app.services.lang import code_to_name
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
            "word": translation,
            "other": other
        })

    return l


def translate_tr(word):
    l = []
    n = 0
    done = False
    # TODO: Some words needs i to be 0 here, investigate at a later time...
    i = 1
    while not done:
        r = translate_cambridge(word + ('' if i == 0 else f'_{i}'), 'tr')
        # TODO: Not perfect but odds that both verb and noun yield the same amount of result and there is another valid position is unlikely
        done = len(r) - n == 0
        n = len(r)
        i += 1
        if not done:
            l += r

    # TODO: this is actually not needed
    def clean_up(entry):
        entry["word"] = remove_punctuation(entry["word"].lower())
        return entry

    return [e for e in l]


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
    if target == 'tr':
        return translate_tr(word)
    elif target == 'zh-Hans':
        return translate_cambridge(word, target_name='chinese-simplified')
    elif target == 'pt':
        return translate_cambridge(word, target_name='portuguese')
    elif target == 'ms':
        return translate_cambridge(word, target_name='malaysian')
    elif target in ['ja', 'ko', 'ar', 'es', 'fr', 'id', 'it', 'pl', 'ca', 'cs', 'da', 'nb', 'ru', 'th', 'vi', 'de']:
        return translate_cambridge(word, target)
    # Last resort, try with Microsoft Translator API
    else:
        return translate_azure(word, target)


def example_sentence(word_src, word_dst, target):
    url = f'https://api.cognitive.microsofttranslator.com/dictionary/lookup?api-version=3.0&from={target}&to=en'
    body = [{'Text': word_dst}]
    response = requests.post(url, headers=get_header('translator'), json=body)
    response_json = json.loads(response.content.decode())[0]

    # the translation from microsoft. need this to use with the dict example. could not match other dictionaries
    microsoft_word_srcs = [e['normalizedTarget']
                           for e in response_json['translations']]

    url = f'{cfg["translator"]["endpoint"]}/Dictionary/Examples?api-version=3.0&from=en&to={target}'

    chosen_src = microsoft_word_srcs[0]
    for src in microsoft_word_srcs:
        if src == word_src:
            chosen_src = word_src

    body = [{
        'Text': chosen_src,
        'Translation': word_dst
    }]
    response = requests.post(url, headers=get_header('translator'), json=body)
    # NOTE: this [0] here is not temporary, doesn't need to be changed
    response = json.loads(response.content.decode())[0]

    def concat_response(entry, source=False):
        pre = "target"
        if source:
            pre = "source"
        return entry[f"{pre}Prefix"] + entry[f'{pre}Term'] + entry[f'{pre}Suffix']

    return [{
        "src_example": concat_response(e, source=True),
        "dst_example": concat_response(e)
    } for e in response['examples']]
