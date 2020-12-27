
import os
from urllib.request import urlopen
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from .config import cfg


def generate_audio(text, target):
    speech_config = SpeechConfig(
        subscription=cfg['speech']['key'], endpoint=cfg['speech']['endpoint'])
    path = os.path.join(os.getcwd(), "app/data/audio", f'{target}-{text}.wav')
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(
        "Customizing audio output format.").get()
    stream = AudioDataStream(result)
    stream.save_to_wav_file(path)
    return 'hi'


def download_audio(recordings):
    for r in recordings:
        tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        path = os.path.join(tmp_dir, r.rsplit('/', 1)[-1])
        with open(path, mode="wb") as f:
            f.write(urlopen(r).read())
