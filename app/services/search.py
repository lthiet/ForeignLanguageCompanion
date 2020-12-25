from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import tempfile
import json
import os
from pathlib import Path


def download_audio(recording):
    tmp_dir = os.path.join(os.getcwd(), "data/tmp")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".ogg", dir=tmp_dir) as f:
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
    return result
