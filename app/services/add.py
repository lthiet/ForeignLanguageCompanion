from enum import unique
from app.services.anki import invoke
from app.services.utils import generate_unique_token
import os
import shutil
import re
import base64
from mimetypes import guess_extension
from threading import Thread
import flask


def fetch_image(path):
    # Copy pasted images
    data_pat = r"data:(image\/.*);base64,(.*)"
    match = re.search(data_pat, path)
    if (not match == None) and len(match.groups()) > 1:
        ext = guess_extension(match[1])
        data = match[2].encode()
        unique_id = 'imagecp-' + generate_unique_token() + ext
        with open(os.path.join(os.getcwd(), 'app/data/images', unique_id), mode='wb') as f:
            f.write(base64.decodebytes(data))
            return 'http://127.0.0.1:5000/image/' + unique_id
    else:
        return path


def create_param_picture(path, kind):
    url = fetch_image(path)
    field_name = {
        "vocabulary": "Picture",
        "pronunciation": "Picture of the example word",
        "sentences": "Front (Picture)",
    }

    return {
        "url": url,
        # "filename": url.strip('/')[-1],
        "filename": generate_unique_token() + '.jpg',
        "fields": [
            field_name[kind]
        ]
    }


def send_add_request(kind, **params):
    has_recording = not params['recording'] == ''
    anki = None
    # if the audio was generated locally
    if params['recording'].startswith('/'):
        params['recording'] = 'http://127.0.0.1:5000' + params['recording']

    if kind == 'vocabulary':
        anki = {
            "note": {
                "deckName": params['deck'],
                "modelName": "2. Picture Words",
                "fields": {
                    "Word": params['word'],
                    "Gender, Personal Connection, Extra Info (Back side)": params['word_usage'],
                    "Pronunciation (Recording and/or IPA)": params['ipa'],
                    "Test Spelling? (y = yes, blank = no)": "y" if params['spelling'] == "true" else ""
                },
                "options": {
                    "allowDuplicate": True,
                },
                "tags": [],
                "audio": [{
                    "url": params['recording'],
                    "filename": generate_unique_token() + '.mp3',
                    "fields": [
                        "Pronunciation (Recording and/or IPA)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url, kind)
                    for url in params['images']]
            }
        }
    elif kind == 'pronunciation':
        anki = {
            "note": {
                "deckName": params['deck'],
                "modelName": "1. Spellings and Sounds",
                "fields": {
                    "Spelling (a letter or combination of letters)": params["spelling"],
                    "Example word for that spelling/sound combination": params["word"],
                    "Recording of the Word (/IPA)": params['ipa']
                },
                "options": {
                    "allowDuplicate": True,
                },
                "tags": [],
                "audio": [{
                    "url": params['recording'],
                    "filename": generate_unique_token() + '.mp3',
                    "fields": [
                        "Recording of the Word (/IPA)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url, kind)
                    for url in params['images']]
            }
        }
    elif kind == 'sentences':
        anki = {
            "note": {
                "deckName": params['deck'],
                "modelName": "3. All-Purpose Card",
                "fields": {
                    "Front (Example with word blanked out or missing)": params["text_hidden"],
                    "Front (Definitions, base word, etc.)": params["front"],
                    "Back (a single word/phrase, no context)": params["text_part"],
                    "- The full sentence (no words blanked out)": params["text_full"],
                    '• Make 2 cards? (y = yes, blank = no)': "y" if params["twocard"] else ''
                },
                "options": {
                    "allowDuplicate": True,
                },
                "tags": [],
                "audio": [{
                    "url": params['recording'],
                    "filename": generate_unique_token() + '.mp3',
                    "fields": [
                        "- Extra Info (Pronunciation, personal connections, conjugations, etc)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url, kind)
                    for url in params['images']]
            }
        }

    return Thread(target=invoke, args=("addNote",), kwargs=anki)
