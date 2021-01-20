from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import requests
import json
import os
from pathlib import Path
from bing_image_downloader import downloader
from app.services.image import download_image
from app.services.lang import code_to_name
from app.services.audio import download_audio
import string


def search(word, target, kind='vocabulary'):
    has_image_api = True
    try:
        image_key = cfg['image']['key']
    except:
        has_image_api = False

    parser = WiktionaryParser()
    # what happens if there are multiple results?
    result = parser.fetch(word, code_to_name(target).lower())
    if len(result) == 0:
        return {
            "word": '',
            "ipas": '',
            "recordings": ''
        }

    result = result[0]

    has_ipa = len(result['pronunciations']['text']) > 0
    has_recording = len(result['pronunciations']['audio']) > 0
    answer = {
        "word": word,
        # "ipas": [e.replace(',', '') for e in result["pronunciations"]["text"][0].split(' ')[1:]] if has_ipa else '',
        "ipas": ', '.join(result["pronunciations"]["text"]),
        "recordings": ['http://localhost:5000/audio/' + download_audio('http:' + e) for e in result['pronunciations']['audio']] if has_recording else ''
    }

    # TODO: is this actually needed?
    def strip_unprintable(data):
        res = ''
        for c in data:
            if not c in ['']:
                res += c
            else:
                res += ' '
        return res

    if kind == 'vocabulary':
        # answer['word_usages'] = [strip_unprintable(
        #     e["partOfSpeech"] + ": " + e["text"][0])for e in result["definitions"]]
        answer['word_usages'] = [e["partOfSpeech"] + ": " + e["text"][0]
                                 for e in result["definitions"]]

    return answer
