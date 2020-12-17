import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter.font import Font
import pandas as pd

word_db = pd.read_csv("data/word_list_debug.csv").sort_values('word')
word_list = word_db.word.to_list()

word = 'clean'
specification = 'adjective'
language = 'arabic'

URL = f'https://dictionary.cambridge.org/dictionary/english-{language}/{word}'
page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(page.content, 'html.parser')
cats = soup.find_all(class_='dlink')
l = []
for c in cats:
    print('hi')
    category = c.find_all(class_='dpos')[0].text

    defs = c.find_all(class_='ddef_d')
    for d in defs:
        definition = d.text
        translation = d.parent.parent.find_all(class_="dtrans")[0].text
        if category == specification or not specification in {'noun', 'adjective', 'verb'}:
            l.append((
                f'{category} / {definition}',
                translation
            ))
print(l)

root = tk.Tk()
current_word_label = tk.Label(text=word_list[0],
                              width=10,
                              height=10)

current_word_label.pack()

frame = tk.Frame(root)
frame.pack()

button = tk.Button(
    text="Next Word",
    width=25,
    height=5
)
root.title("App")

button.pack()

for e in l:
    # The button that display the category of the english word and its english definition
    label_catdef = tk.Label(frame, text=e[0])
    label_catdef.pack()

    btn_trans = tk.Button(frame, text=e[1])
    btn_trans.pack()


def handle_click(event):
    handle_click.i += 1
    handle_click.i = handle_click.i % word_db.shape[0]
    current_word_label['text'] = word_list[handle_click.i]


handle_click.i = 0
button.bind("<Button-1>", handle_click)
root.mainloop()
