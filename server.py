from base64 import b64decode
import flask
from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from flask import jsonify
import os
import pandas as pd
from app.services.translate import example_sentence, translate_word, make_translation
from app.services.search import search
from app.services.add import send_add_request
from app.services.anki import invoke
from app.services.image import download_image, save_image
from app.services.lang import lang_code
from app.services.audio import generate_audio
from app.services.sentence import process_sentence
from app.services.nlp import lemmatize
import threading
import glob
from pathlib import Path



threads = [threading.Thread]

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static'
            )
app.config['SECRET_KEY'] = 'abcd'
bootstrap = Bootstrap(app)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/vocabulary/')
def vocabulary():
    decks = invoke("deckNames")

    path = os.path.join(os.getcwd(), 'app/data/word_list')
    word_list = []
    for wl in glob.glob(path + '/**/*.csv', recursive=True):
        p = Path(wl)
        pname = p.name
        pparent = p.parent.name
        word_list.append(Path(pparent, pname))

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
    return render_template('translate.html', translations=translations)


@app.route('/vocabulary/search')
def vocabulary_search():
    word = request.args.get('word')
    target = request.args.get('target')

    # TODO: some words have commas in them, not sure why
    # word = word.replace(',', '').replace(';', '')

    result = search(word, target, kind='vocabulary')
    return render_template('search.html', kind="vocabulary", **result)


@app.route('/image/<id>')
def get_image(id):
    path = os.path.join(os.getcwd(), f'app/data/images/{id}')
    return send_file(path)


@app.route('/vocabulary/add')
def vocabulary_add():
    params = dict(request.args)
    params['images'] = request.args.getlist('images[]')
    params.pop('images[]', None)
    thread = send_add_request('vocabulary', **params)
    thread.start()
    threads.append(thread)
    return str(thread.ident)


@app.route('/vocabulary/word_list')
def vocabulary_word_list():
    word_list = request.args['word_list']
    words = pd.read_csv(os.path.join(
        os.getcwd(), 'app/data/word_list', word_list), header=None)[0].to_list()
    is_en = Path(word_list).parent.name == 'en'
    return render_template('word_list.html', words=words, is_en=is_en)


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
    return send_add_request('pronunciation', **params)


@app.route("/image_search")
def image_search():
    word = request.args.get('word')
    offset = int(request.args.get('offset'))
    target = request.args.get('target')
    n = 100
    paths = download_image(
        word, target=target, offset=offset, n=n)
    params = {
        "word": word,
        "n": n,
        "offset": offset,
        "paths": paths,
        "from_copy": False
    }
    return render_template('image_search_result.html', **params)


@app.route("/image/upload", methods=['POST'])
def image_upload():
    data64 = request.get_data().decode()
    img_url = 'http://localhost:5000/image/' + save_image(data64)
    path = {
        "thumbnail_url": img_url,
        "content_url": img_url,
    }
    return render_template('image_search_result.html', paths=[path], from_copy=True)


@app.route("/audio/add")
def audio_add():
    word = request.args.get('word')
    target = request.args.get('target')
    path = generate_audio(word, target)
    return render_template('add_audio_result.html', path=path)


@app.route("/audio/<fn>")
def audio(fn):
    path = os.path.join(os.getcwd(), "app/data/audio", fn)
    return send_file(path)


@app.route("/sentences/")
def sentences(example=None, definition=None):
    params = {
        "decks":  invoke("deckNames"),
        "lang_code": lang_code,

        # From abstract words
        "example": example,
        "definition": definition
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
    guess_syntax = params['guess_syntax'] == 'true'
    params['twocard'] = params['twocard'] == 'true'
    params['text_hidden'] = process_sentence(
        text_full, text_part, guess_syntax)
    params['images'] = request.args.getlist('images[]')
    params.pop('images[]', None)

    if guess_syntax:
        params['front'] = params['text_part']
        params['text_part'] = ''
        params['twocard'] = False

    # TODO: factorize
    thread = send_add_request('sentences', **params)
    thread.start()
    threads.append(thread)
    return str(thread.ident)


# @app.route('/vocabulary/abstract_word/')
# def abstract_word():
#     req = request.args
#     word_src = req.get("word_src")
#     word_dst = req.get("word_dst")
#     target = req.get("target")
#     detail = req.get("detail")
#     res = get_abstract_word(word_src, word_dst, target, detail)
#     return sentences(example=res["examples"][0] if len(res["examples"]) > 0 else '', definition=res["definition"])


@app.route('/thread_status/<ident>')
def check_thread_status(ident):
    ident = int(ident)
    for t in threads:
        if t.ident == ident:
            if t.is_alive():
                return "running"
            else:
                return "done"
    return "not found"


@app.route('/lemmatizer/')
def lemmatizer():
    req = request.args
    word = req.get('word')
    target = req.get('target')
    return lemmatize(word, target)


@app.route('/vocabulary/examples')
def vocabulary_examples():
    req = request.args
    word_src = req.get('word_src')
    word_dst = req.get('word_dst')
    target = req.get('target')
    return jsonify(example_sentence(word_src, word_dst, target))


@app.route('/translate/')
def translate():
    req = request.args
    text = req.get('text')
    src = req.get('src')
    dst = req.get('dst')
    return make_translation(text, src, dst)