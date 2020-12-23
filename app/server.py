from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template
from flask import request
from services.vocab import translate_word
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
bootstrap = Bootstrap(app)


@app.route('/vocabulary/')
def vocabulary():
    return render_template('vocabulary.html')


@app.route('/vocabulary/translate')
def vocabulary_translate():
    word = request.args.get('word')
    print(request.args)
    translations = translate_word(word)
    return render_template('vocabulary_translate_result.html', translations=translations)
