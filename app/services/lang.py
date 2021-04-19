from app.services.config import cfg, get_token
import requests
import json
import collections
import random

# Get list of speaker
speakers = json.loads(requests.get("https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list", headers={
    "Authorization": "Bearer " + get_token()
}).content)

mapping_of_speakers = collections.defaultdict(list)
for e in speakers:
    print(e)
    if e["VoiceType"] == "Neural" and e["Gender"] == "Female": # for some reason male voices are broken
        mapping_of_speakers[e["Locale"][:2]].append({
            "name": e["ShortName"],
            "gender": e["Gender"],
            "country": e["Locale"][3:]
        })


# Get list of available languages for translation
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
    # language specific answer
    if code.startswith('zh'):
        return "Chinese"
    for o in lang_code:
        if code == o['code']:
            return o['name']
    print('WARNING CODE NOT FOUND')


def target_to_voice_name(target):
    if target.startswith('zh'):
        target = 'zh'

    avai_speakers = mapping_of_speakers[target]
    speaker = random.choice(avai_speakers)["name"]
    return speaker


def lang_to_mkt(target):
    mapping = {
        'tr': 'tr-TR',
        'de': 'de-DE',
        'es': 'es-ES',
    }

    try:
        return mapping[target]
    except KeyError:
        return target 
