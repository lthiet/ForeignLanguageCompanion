from enum import unique
from .anki import invoke
from .utils import generate_unique_token
import os
import shutil
import re
import base64
from mimetypes import guess_extension


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


def create_param_picture(path):
    url = fetch_image(path)
    return {
        "url": url,
        "filename": url.strip('/')[-1],
        "fields": [
            "Picture"
        ]
    }


def add(kind, **params):
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
                    "Test Spelling? (y = yes, blank = no)": "y" if params['spelling'] else ""
                },
                "options": {
                    "allowDuplicate": True,
                },
                "tags": [],
                "audio": [{
                    "url": params['recording'],
                    "filename": params['recording'].strip('/')[-1],
                    "fields": [
                        "Pronunciation (Recording and/or IPA)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url)
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
                    "filename": params['recording'].strip('/')[-1],
                    "fields": [
                        "Recording of the Word (/IPA)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url)
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
                    # "• Make 2 cards? (\"y\" = yes, blank = no)": "y"
                },
                "tags": [],
                "audio": [{
                    "url": params['recording'],
                    "filename": params['recording'].strip('/')[-1],
                    "fields": [
                        "- Extra Info (Pronunciation, personal connections, conjugations, etc)"
                    ]
                }] if has_recording else None,
                "picture": [
                    create_param_picture(url)
                    for url in params['images']]
            }
        }

    note_id = invoke("addNote", **anki)

    # Delete file used
    path = os.path.join(os.getcwd(), 'app/data')

    def delete(x):
        if os.path.exists(os.path.join(path, x)):
            shutil.rmtree(os.path.join(path, x))

    pathaudio = os.path.join(path, 'audio')
    pathimage = os.path.join(path, 'images')
    delete(pathaudio)
    delete(pathimage)
    return str(note_id)
