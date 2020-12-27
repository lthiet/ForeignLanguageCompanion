from .config import cfg
import requests
import json

url = "https://api.cognitive.microsofttranslator.com/languages?api-version=3.0"
response = requests.get(url)
response = json.loads(response.content.decode())["dictionary"]
lang_code = []
for (k, v) in response.items():
    lang_code.append({
        "code": k,
        "name": v["name"],
        "native_name": v["nativeName"]
    })


def code_to_name(code):
    # language specific answer
    if code.startswith('zh'):
        return "Chinese"
    for o in lang_code:
        if code == o['code']:
            return o['name']
    print('WARNING CODE NOT FOUND')


def target_to_voice_name(target):
    # TODO: this was done by hand, there's probably a programmatic way to do this
    # language specific
    if target.startswith('zh'):
        target = 'zh'

    mapping_female = {
        "ar": "ar-SA-ZariyahNeural",
        "bg": "bg-BG-KalinaNeural",
        "ca": "ca-ES-JoanaNeural",
        "zh": "zh-CN-XiaohanNeural",
        "hr": "hr-HR-GabrijelaNeural",
        "cs": "cs-CZ-VlastaNeural",
        "da": "da-DK-ChristelNeural",
        "nl": "nl-NL-ColetteNeural",
        "en": "en-US-AriaNeural",
        "fi": "fi-FI-SelmaNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "el": "el-GR-AthinaNeural",
        "he": "he-IL-HilaNeural",
        "hi": "hi-IN-SwaraNeural",
        "hu": "hu-HU-NoemiNeural",
        "id": "id-ID-GadisNeural",
        "it": "it-IT-ElsaNeural",
        "ja": "ja-JP-NanamiNeural",
        "ko": "ko-KR-SunHiNeural",
        "ms": "ms-MY-YasminNeural",
        "nb": "nb-NO-IselinNeural",
        "pl": "pl-PL-AgnieszkaNeural",
        "pt": "pt-PT-FernandaNeural",
        "ro": "ro-RO-AlinaNeural",
        "ru": "ru-RU-DariyaNeural",
        "sk": "sk-SK-ViktoriaNeural",
        "sl": "sl-SI-PetraNeural",
        "es": "es-ES-ElviraNeural",
        "sv": "sv-SE-SofieNeural",
        "ta": "ta-IN-PallaviNeural",
        "te": "te-IN-ShrutiNeural",
        "th": "th-TH-AcharaNeural",
        "tr": "tr-TR-EmelNeural",
        "vi": "vi-VN-HoaiMyNeural",
    }
    mapping_male = {
        # TODO: todo
    }
    return mapping_female[target]
