from app.services.lang import lang_to_mkt
from app.services.config import cfg
from app.services.utils import generate_unique_token
import trace
from requests.models import HTTPError
import traceback
from bing_image_downloader import downloader
from PIL import Image
from io import BytesIO
import requests
import os
import pybase64


has_api = True
try:
    cfg['image']['key']
except:
    has_api = False

MAX_SIZE = (600, 600)


def get_images_path(unique_id):
    path = os.path.join(os.getcwd(), "app/data/images/")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    im_path = os.path.join(
        path, unique_id)
    return im_path


def save_image(data64):
    header, encoded = data64.split(",", 1)
    unique_id = f"image-copypaste-{generate_unique_token()}.jpg"
    im_path = get_images_path(unique_id)
    data = pybase64.b64decode(encoded, validate=True)
    im = Image.open(BytesIO(data))
    im = im.convert('RGB')
    im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    im.save(im_path, 'JPEG')
    return unique_id


def download_images_azure(word, target=None, offset=0, n=10):
    key = cfg['image']['key']
    url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "BingAPIs-Market": lang_to_mkt(target)
    }
    # TODO : some parameters are interesting here https://docs.microsoft.com/en-us/bing/search-apis/bing-image-search/reference/query-parameters, for example tags
    params = {"q": word,
              "license": "All",
              "offset": offset,
              "setLang": target,
              "mkt": lang_to_mkt(target),
              "count": n,
              # "safeSearch": "Strict" # so tired of porn showing up...
              }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    paths = []
    maxn = len(search_results["value"])
    for i in range(min(n, maxn)):
        paths.append({
            "thumbnail_url": search_results["value"][i]["thumbnailUrl"],
            "content_url": search_results["value"][i]["contentUrl"],
        })
    return paths

    # if I want to save the images, but do I really want to?
    id_list = []
    for i, turl in enumerate(thumbnail_urls):
        image_data = requests.get(turl)
        im = Image.open(BytesIO(image_data.content))
        unique_id = f"image-{target}-{generate_unique_token()}"
        im_path = get_images_path(unique_id)
        im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
        im.save(im_path, "JPEG")
        id_list.append(unique_id)

    return id_list


def download_image(word, target=None, offset=0, n=10):
    try:
        return download_images_azure(word, target, offset, n)
    except HTTPError:
        traceback.print_exc()
        return []
        # traceback.print_exc()
        # downloader.download(word, limit=5,  output_dir='app/data/images',
        # adult_filter_off=True, force_replace=False, timeout=1)
