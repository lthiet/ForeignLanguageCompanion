from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import json
import os
from pathlib import Path
from bing_image_downloader import downloader


def download_image(word):
    downloader.download(word, limit=5,  output_dir='app/data/images',
                        adult_filter_off=True, force_replace=False, timeout=1)


def download_audio(recording):
    tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    path = os.path.join(tmp_dir, recording.rsplit('/', 1)[-1])
    with open(path, mode="wb") as f:
        f.write(urlopen(recording).read())
        return f.name


def search(word):
    parser = WiktionaryParser()
    result = parser.fetch(word, 'german')[0]
    has_ipa = len(result['pronunciations']['text']) > 0
    has_recording = len(result['pronunciations']['audio']) > 0
    result = {
        "word": word,
        "ipas": [e.replace(',', '') for e in result["pronunciations"]["text"][0].split(' ')[1:]] if has_ipa else '',
        "word_usages": [e["partOfSpeech"] + ": " + e["text"][0] for e in result["definitions"]],
        "recordings": ["https:" + e for e in result['pronunciations']['audio']] if has_recording else ''
    }
    download_image(word)
    download_audio(result['recordings'][0])
    return result
