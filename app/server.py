from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from services.translate import translate_word
from services.search import search
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
    result = search(word)
    ipas = result['ipas']
    word_usages = result['word_usages']
    return render_template('vocabulary_search_result.html', ipas=ipas, word_usages=word_usages)
