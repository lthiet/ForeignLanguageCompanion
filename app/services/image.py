from .config import cfg
from bing_image_downloader import downloader
from .config import cfg
from PIL import Image
from io import BytesIO
import requests
import os

has_api = True
try:
    cfg['image']['key']
except:
    has_api = False


def download_image(word, target=None, offset=0, n=10):
    if has_api:
        key = cfg['image']['key']
        location = cfg['image']['location']
        url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": key}
        # TODO : some parameters are interesting here https://docs.microsoft.com/en-us/bing/search-apis/bing-image-search/reference/query-parameters, for example tags
        params = {"q": word,
                  "license": "All",
                  "offset": offset,
                  "setLang": target,
                  # TODO: change this to any language
                  "mkt": "de-DE",
                  "count": n,
                  }
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
            im.save(os.path.join(path, f"Image_{i+1+int(offset)}.png"), "PNG")
    else:
        downloader.download(word, limit=5,  output_dir='app/data/images',
                            adult_filter_off=True, force_replace=False, timeout=1)
