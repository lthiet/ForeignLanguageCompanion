from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import requests
import json
import os
from pathlib import Path
from bing_image_downloader import downloader
from .image import download_image
from .lang import code_to_name


def download_audio(recording):
    tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    path = os.path.join(tmp_dir, recording.rsplit('/', 1)[-1])
    with open(path, mode="wb") as f:
        f.write(urlopen(recording).read())
        return f.name


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
    if kind == 'vocabulary':
        answer['word_usages'] = [e["partOfSpeech"] + ": " + e["text"][0]
                                 for e in result["definitions"]],

    if has_recording:
        download_audio(answer['recordings'][0])
    return answer
