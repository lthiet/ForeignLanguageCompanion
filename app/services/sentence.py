from app.services.config import cfg
import requests
import json


def process_sentence(text_full, text_part, guess_syntax):
    i = text_full.find(text_part)
    replacement = '' if guess_syntax else '[...]'
    return text_full[:i] + replacement + text_full[i+len(text_part):]


def translate(text, target):
    key = cfg['translator']['key']
    location = cfg['translator']['location']
    url = f'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from=en&to={target}'
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
    }
    body = [{
        'Text': text
    }]
    response = requests.post(url, headers=headers, json=body)
    response = json.loads(response.content.decode())
    return response[0]['translations'][0]['text']




