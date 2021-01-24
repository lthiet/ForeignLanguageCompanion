# ForeignLanguageCompanion

This project aims to be a supplement to your language learning journey. Its main goal is to speed up
the mundane processes that one can find while learning a new language. These includes, looking up a word,
searching for corresponding images, finding a recording, and so on. These tasks can take quite a
lot of time if done manually. The project automates almost any part that does not fundamentally require
human action. 

The book [Fluent Forever](https://www.amazon.de/Fluent-Forever-Learn-Language-Forget/dp/0385348118)
by Gabriel Wyner was the main inspiration of this project. You will notice that virtually every design
choice was made according to this book. It is advised to have read this book or at least the *Toolbox*
chapter to fully appreciate this work. Depending on your use case, the 
[official app](https://fluent-forever.com/app/) might be more suited to you.
However, If any of these describes you, then you might be more interested into my own implementation : 

- Learning a Language that the official app does not support
- Prefer to work with the Anki ecosystem
- Short on money

Another salient characteristics of this work is the use of state-of-the-art natural language
understanding methods to generate content (recordings, translation, etc.) that replaces human-made
content when the latter is not readily available or well structured. While the effect of using
computer-generated content as reference to your own learning has not been largely studied (or
my googling and research skill clearly needs some sharpening), it is still paramount to 
remember that machine prediction is not perfectly accurate.
Consequently, whenever human-made content is available,
it is preferred to the machine-made content.

## Implemented Features
- Vocabulary, Pronunciation, Fill-in-the-blank sentences
- Image Lookup
- Dictionary Translation
- Machine Translation
- Word Usage, Pronunciation, IPA
- Text-to-speech

## Features to come
- Abstract definitions
- Syntax sentences
- Machine transliteration

### Note on Language Learning

Even though it is stated that this tool is a **supplement** to language learning, it is possible
that it might be confused with a do-it-all-for-you language learning app. It is **not** the case.
Most of the effort will still have to come from you (until brains can be plugged into computers). The
reader is invited to refer to other sources for language learning in the general sense. This tool
is made solely for the purpose of automating flashcards creation. The relevance or justification
of a flashcard to learn a specific aspect of a language has to be inferred from the
reader's judgement.
# Installation

## API Keys

This program uses [Azure](https://azure.microsoft.com/en-us/) as the backbone for machine translation,
image look up text-to-speech functionalities. You can use these services for free up to 100$ if you are
a student. The services remains free if you do not go over your quota. Please refer
to their documentation in order to get your API keys.

The process might loosely look like this :
1. Create an account
2. Enter payment details 
3. Create service
4. Get the API key 

You will need the following services : 
- Speech
- Translator
- Bing Search

Once you have set up these services, create a `config.ini` file : 

```shell
touch config.ini
```
And fill in your credentials. These can be found under the "Keys and Endpoint" section under "Resource
Management"

```ini
[speech]
key=...
location=...
endpoint=...
[image]
key=...
location=...
endpoint=...
[translator]
key=...
location=...
endpoint=...
```


## Prerequisites


You will need the following :
- [Anki](https://apps.ankiweb.net/)
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
- [Python](https://docs.conda.io/en/latest/miniconda.html)
- [Fluent Forever Model Deck](http://fluent-forever.com/downloads/Model-Deck-May-2014.apkg.zip) 
- [Some motivation](https://cdn.statically.io/img/nextshark.com/wp-content/uploads/2017/12/Never-Give-Up.png?quality=80&f=auto) 

You will find tutorial on how to install each of these in their respective documentation.
Once you have gathered all of the above, you will need the dependencies : 


```shell
pip install -r requirements.txt
```

You will also need this package

```shell
sudo apt install ffmpeg
```

Now you may use the program.

## Step-by-step
1. Open Anki
2. Download the repo 
```
git clone https://github.com/truvaking/ForeignLanguageCompanion.git
```
3. Go into the repo root directory
```
cd ForeignLanguageCompanion
```
4. Make the shell script executabe
```shell
chmod +x ./start.sh
```

5. Run it.
```shell
./start.sh
```

6. On your browser, go to this url : http://127.0.0.1:5000/

That's it! Now choose whichever type of card you want to create and fill in the blank, click
buttons as you go. 

# Tutorial

[![demo video](https://img.youtube.com/vi/X6vQfZ7opCM/0.jpg)](https://youtu.be/X6vQfZ7opCM)