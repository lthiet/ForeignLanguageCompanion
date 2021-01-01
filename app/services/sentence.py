from .config import cfg, get_header
import requests
import json


def process_sentence(text_full, text_part):
    i = text_full.find(text_part)
    return text_full[:i] + '[...]' + text_full[i+len(text_part):]


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


def example_sentence(word_dst, word_src, target):
    url = f'{cfg["translator"]["endpoint"]}/Dictionary/Examples?api-version=3.0&from=en&to={target}'
    body = [{
        'text': word_dst,
        'translation': word_src
    }]
    response = requests.post(url, headers=get_header('translator'), json=body)
    response = json.loads(response.content.decode())[0]

    def concat_response(entry):
        return entry["targetPrefix"] + entry['targetTerm'] + entry['targetSuffix']
    return [concat_response(e) for e in response["examples"]]


def get_abstract_word(word_dst, word_src, target, detail):
    _, position, definition = tuple(detail.split(' / '))

    # Step 1 : Translate definition and position
    definition = translate(definition, target)
    position = translate(position, target)

    # Step 2 : Get example sentences
    examples = example_sentence(word_dst, word_src, target)
    return {
        "definition": position + ": " + definition,
        "examples": examples
    }
