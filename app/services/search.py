from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import requests
import json
import os
from pathlib import Path
from bing_image_downloader import downloader
from .image import download_image
from .lang import code_to_name
from .audio import download_audio
import string


def search(word, target, kind='vocabulary'):
    has_image_api = True
    try:
        image_key = cfg['image']['key']
    except:
        has_image_api = False

    parser = WiktionaryParser()
    # what happens if there are multiple results?
    result = parser.fetch(word, code_to_name(target).lower())[0]

    has_ipa = len(result['pronunciations']['text']) > 0
    has_recording = len(result['pronunciations']['audio']) > 0
    answer = {
        "word": word,
        "ipas": [e.replace(',', '') for e in result["pronunciations"]["text"][0].split(' ')[1:]] if has_ipa else '',
        "recordings": ["https:" + e for e in result['pronunciations']['audio']] if has_recording else ''
    }

    def strip_unprintable(data):
        res = ''
        for c in data:
            if c in string.printable:
                res += c
            else:
                res += ' '
        return res

    if kind == 'vocabulary':
        answer['word_usages'] = [strip_unprintable(e["partOfSpeech"] + ": " + e["text"][0])
                                 for e in result["definitions"]]

    print(answer['word_usages'])

    if has_recording:
        download_audio(answer['recordings'])
    return answer
