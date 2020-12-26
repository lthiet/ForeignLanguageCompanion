from wiktionaryparser import WiktionaryParser
from urllib.request import urlopen
import requests
import json
import os
from pathlib import Path
from bing_image_downloader import downloader
from .config import cfg
from PIL import Image
from io import BytesIO


def download_image(word, n=3, has_api=False):
    if has_api:
        key = cfg['image']['key']
        location = cfg['image']['location']
        url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": key}
        # TODO : any language
        # TODO : some parameters are interesting here https://docs.microsoft.com/en-us/bing/search-apis/bing-image-search/reference/query-parameters, for example tags
        params = {"q": word, "license": "All",
                  "cc": "DE", "count": n, "setLang": "de"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"]
                          for img in search_results["value"][:n]]
        for i, turl in enumerate(thumbnail_urls):
            image_data = requests.get(turl)
            im = Image.open(BytesIO(image_data.content))
            path = os.path.join(os.getcwd(), "app/data/images/",
                                word)
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            im.save(os.path.join(path, f"Image_{i+1}.jpg"), "JPEG")
    else:
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


def search(word, kind='vocabulary'):
    has_image_api = True
    try:
        image_key = cfg['image']['key']
    except:
        has_image_api = False

    parser = WiktionaryParser()
    # what happens if there are multiple results?
    result = parser.fetch(word, 'german')[0]
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

    download_image(word, has_api=has_image_api)
    if has_recording:
        download_audio(answer['recordings'][0])
    return answer
