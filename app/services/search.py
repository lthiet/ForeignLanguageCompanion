from wiktionaryparser import WiktionaryParser
import json


def search(word):
    parser = WiktionaryParser()
    result = parser.fetch(word, 'german')[0]
    result = {
        "ipas": [e.replace(',', '') for e in result["pronunciations"]["text"][0].split(' ')[1:]],
        "word_usages": [e["partOfSpeech"] + ": " + e["text"][0] for e in result["definitions"]],
        "recordings": [e for e in result['pronunciations']['audio']]
    }
    return result
