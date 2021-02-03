from flask.globals import request
import nltk
from nltk.stem.cistem import Cistem
from nltk.stem.snowball import GermanStemmer
import spacy
nlp = spacy.load("de_core_news_sm")
stemmer1 = GermanStemmer()
stemmer2 = Cistem()


def lemmatize(text, target):
    if target == 'de':
        r = []
        for t in nlp(text):
            # r.append(stemmer1.segment(t)[0])
            # r.append(stemmer1.stem(t))
            r.append(t.lemma_)

        return ', '.join(r)

    return ''
