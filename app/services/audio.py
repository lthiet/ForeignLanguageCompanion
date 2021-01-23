
from enum import unique
import os
from urllib.request import urlopen
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from app.services.config import cfg
from app.services.lang import target_to_voice_name
from app.services.utils import generate_unique_token
import subprocess
from pathlib import Path


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
    unique_id = f'audio-{target}-{generate_unique_token()}.mp3'
    path = os.path.join(
        tmp_dir, unique_id)

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


def download_audio(recording):
    tmp_dir = os.path.join(os.getcwd(), "app/data/audio")
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    unique_id = generate_unique_token()
    path = os.path.join(tmp_dir, unique_id + ".ogg")
    with open(path, mode="wb") as f:
        f.write(urlopen(recording).read())
    new_path, _ = os.path.splitext(path)
    new_path = Path(new_path).with_suffix('.mp3')
    subprocess.run(["ffmpeg", "-loglevel", "panic", "-y", "-i", path, new_path])
    os.remove(path)
    return new_path.name
