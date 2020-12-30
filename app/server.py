from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import glob
import os
import pandas as pd
from app.services.translate import translate_word
from app.services.search import search
from app.services.add import add
from app.services.anki import invoke
from app.services.image import download_image
from app.services.lang import lang_code
from app.services.audio import generate_audio
from app.services.sentence import process_sentence
app = Flask(__name__, template_folder="app/templates",
            static_folder="app/static")
app.config['SECRET_KEY'] = 'abcd'
bootstrap = Bootstrap(app)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/vocabulary/')
def vocabulary():
    decks = invoke("deckNames")
    path = os.path.join(os.getcwd(), 'app/data/word_list')
    word_list = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    params = {
        "decks": decks,
        "word_list": word_list,
        "lang_code": lang_code}
    return render_template('vocabulary.html', **params)


@app.route('/vocabulary/translate')
def vocabulary_translate():
    word = request.args.get('word')
    target = request.args.get('target')
    translations = translate_word(word, target)
    return render_template('vocabulary_translate_result.html', translations=translations)


@app.route('/vocabulary/search')
def vocabulary_search():
    word = request.args.get('word')
    target = request.args.get('target')

    # TODO: some words have commas in them, not sure why
    word = word.replace(',', '').replace(';', '')

    result = search(word, target, kind='vocabulary')

    return render_template('search_result.html', kind="vocabulary", **result)


@app.route('/image/<word>/<i>')
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
    return add('vocabulary', **params)


@app.route('/vocabulary/word_list')
def vocabulary_word_list():
    word_list = request.args['word_list']
    words = pd.read_csv(os.path.join(
        os.getcwd(), 'app/data/word_list', word_list), header=None)[0].to_list()
    return render_template('word_list.html', words=words)


@app.route('/pronunciation/')
def pronunciation():
    params = {
        "decks": invoke("deckNames"),
        "lang_code": lang_code
    }
    return render_template('pronunciation.html', **params)


@app.route('/pronunciation/search')
def pronunciation_search():
    word = request.args.get('word')
    target = request.args.get('target')
    result = search(word, target, kind="pronunciation")
    return render_template('search_result.html', kind="pronunciation", **result)


@app.route("/pronunciation/add")
def pronunciation_add():
    params = dict(request.args)
    params['images'] = request.args.getlist('images[]')
    params.pop('images[]', None)
    return add('pronunciation', **params)


@app.route("/image_search")
def image_search():
    word = request.args.get('word')
    offset = int(request.args.get('offset'))
    target = request.args.get('target')
    n = 5
    download_image(word, target=target, offset=offset, n=n)
    params = {
        "word": word,
        "n": n,
        "offset": offset
    }
    return render_template('image_search_result.html', **params)


@app.route("/audio/add")
def audio_add():
    word = request.args.get('word')
    target = request.args.get('target')
    generate_audio(word, target)
    path = f"/audio/{target}/{word}"
    return render_template('add_audio_result.html', path=path)


@app.route("/audio/<target>/<word>")
def audio(target, word):
    path = os.path.join(os.getcwd(), "app/data/audio", f"{target}-{word}.wav")
    return send_file(path)


@app.route("/sentences/")
def sentences():
    params = {
        "decks":  invoke("deckNames"),
        "lang_code": lang_code
    }
    return render_template('sentences.html', **params)


@app.route("/sentences/search/")
def sentences_search():
    return render_template('select_sentence_result.html', kind="sentences")


@app.route("/sentences/add/")
def sentences_add():
    text_full = request.args.get('text_full')
    text_part = request.args.get('text_part')
    params = dict(request.args)
    params['text_hidden'] = process_sentence(text_full, text_part)
    params['images'] = request.args.getlist('images[]')
    params.pop('images[]', None)
    return add('sentences', **params)


if __name__ == '__main__':
    app.run()
