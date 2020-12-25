from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import glob
import os
from services.translate import translate_word
from services.search import search
from services.add import add
from services.anki import invoke
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
bootstrap = Bootstrap(app)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/vocabulary/')
def vocabulary():
    decks = invoke("deckNames")
    return render_template('vocabulary.html', decks=decks)


@app.route('/vocabulary/translate')
def vocabulary_translate():
    word = request.args.get('word')
    translations = translate_word(word)
    return render_template('vocabulary_translate_result.html', translations=translations)


@app.route('/vocabulary/search')
def vocabulary_search():
    word = request.args.get('word')

    # TODO: some words have commas in them, not sure why
    word = word.replace(',', '').replace(';', '')

    result = search(word)
    return render_template('vocabulary_search_result.html', **result)


@app.route('/vocabulary/image/<word>/<i>')
def vocabulary_image(word, i):
    path = os.path.join(os.getcwd(), f'app/data/images/{word}/')
    for infile in glob.glob(os.path.join(path, f'Image_{i}.*')):
        # TODO: there should be only one
        return send_file(infile)


@app.route('/vocabulary/add')
def vocabulary_add():
    params = dict(request.args)
    params['images'] = request.args.getlist('images[]')
    params.pop('images[]', None)
    return add(**params)
