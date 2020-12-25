from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
from services.translate import translate_word
from services.search import search
from services.add import add
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
bootstrap = Bootstrap(app)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/vocabulary/')
def vocabulary():
    return render_template('vocabulary.html')


@app.route('/vocabulary/translate')
def vocabulary_translate():
    word = request.args.get('word')
    translations = translate_word(word)
    return render_template('vocabulary_translate_result.html', translations=translations)


@app.route('/vocabulary/search')
def vocabulary_search():
    word = request.args.get('word')

    # TODO: some words have commas in them, not sure why
    word = word.replace(',', '')

    result = search(word)
    return render_template('vocabulary_search_result.html', **result)


@app.route('/vocabulary/image/<word>/<i>')
def vocabulary_image(word, i):
    return send_file(f"data/images/{word}/Image_{i}.jpg", mimetype='image/jpg')


@app.route('/vocabulary/add')
def vocabulary_add():
    return str(add())
