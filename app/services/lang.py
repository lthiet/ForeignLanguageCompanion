from .config import cfg
import requests
import json

url = "https://api.cognitive.microsofttranslator.com/languages?api-version=3.0"
response = requests.get(url)
response = json.loads(response.content.decode())["dictionary"]
lang_code = []
for (k, v) in response.items():
    lang_code.append({
        "code": k,
        "name": v["name"],
        "native_name": v["nativeName"]
    })


def code_to_name(code):
    for o in lang_code:
        if code == o['code']:
            return o['name']
    print('WARNING CODE NOT FOUND')
