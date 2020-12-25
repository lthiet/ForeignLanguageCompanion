from .anki import invoke
import os
import shutil


def add(**params):
    anki = {
        "note": {
            "deckName": params['deck'],
            "modelName": "2. Picture Words",
            "fields": {
                "Word": params['word'],
                "Gender, Personal Connection, Extra Info (Back side)": params['word_usage'],
                "Pronunciation (Recording and/or IPA)": params['ipa'],
                "Test Spelling? (y = yes, blank = no)": ""
            },
            "tags": [],
            "audio": [{
                "url": params['recording'],
                "filename": params['recording'].strip('/')[-1],
                "fields": [
                    "Pronunciation (Recording and/or IPA)"
                ]
            }],
            "picture": [{
                "url": url,
                "filename": url.strip('/')[-1],
                "fields": [
                    "Picture"
                ]
            } for url in params['images']]
        }
    }

    note_id = invoke("addNote", **anki)

    # Delete file used
    path = os.path.join(os.getcwd(), 'app/data')
    shutil.rmtree(os.path.join(path, 'audio'))
    shutil.rmtree(os.path.join(path, 'images'))
    return str(note_id)
