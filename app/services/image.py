from .config import cfg
from bing_image_downloader import downloader
from PIL import Image
from io import BytesIO
import requests
import os
from .utils import generate_unique_token

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
                  "mkt": target,
                  "count": n,
                  }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"]
                          for img in search_results["value"][:n]]
        id_list = []
        for i, turl in enumerate(thumbnail_urls):
            image_data = requests.get(turl)
            im = Image.open(BytesIO(image_data.content))
            path = os.path.join(os.getcwd(), "app/data/images/")
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            unique_id = f"image-{target}-{generate_unique_token()}"
            im_path = os.path.join(
                path, unique_id + ".jpg")
            im.save(im_path, "JPEG")
            id_list.append(unique_id)
        return id_list
    else:
        downloader.download(word, limit=5,  output_dir='app/data/images',
                            adult_filter_off=True, force_replace=False, timeout=1)
