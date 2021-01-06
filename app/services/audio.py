
import os
from urllib.request import urlopen
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from .config import cfg
from .lang import target_to_voice_name
from .utils import generate_unique_token


def create_ssml(text, target):

    # TODO : can specify IPA here
    ssml = f"""<?xml version='1.0' encoding='UTF-8'?>
    <speak xmlns="https://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="{target}">
        <voice name="{target_to_voice_name(target)}">
            {text} 
        </voice>
    </speak>
    """
    return ssml


def generate_audio(text, target):
    # create the path
    tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    unique_id = f'audio-{target}-{generate_unique_token()}'
    path = os.path.join(
        tmp_dir, unique_id + '.wav')

    # query the API
    speech_config = SpeechConfig(
        subscription=cfg['speech']['key'], region=cfg['speech']['location'])
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat["Audio24Khz96KBitRateMonoMp3"])
    ssml_string = create_ssml(text, target)
    audio_config = AudioOutputConfig(filename=path)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_ssml(ssml_string)
    return unique_id


def download_audio(recordings):
    for r in recordings:
        tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        path = os.path.join(tmp_dir, r.rsplit('/', 1)[-1])
        with open(path, mode="wb") as f:
            f.write(urlopen(r).read())
