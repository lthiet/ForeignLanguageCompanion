from app.services.config import get_token, cfg
import requests
import json
import collections

header = {
    "Authorization": "Bearer " + get_token()
}
test = requests.get(
    "https://eastus.tts.speech.microsoft.com/cognitiveservices/voices/list", headers=header)
l = json.loads(test.content)

d = collections.defaultdict(list)

for e in l:
    if e["VoiceType"] == "Neural":
        d[e["Locale"][:2]].append({
            "name": e["ShortName"],
            "gender": e["Gender"],
            "country": e["Locale"][3:]
        })
