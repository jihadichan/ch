import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

from pathlib import Path

import azure.cognitiveservices.speech as speechsdk

from src.utils import FileUtils


class RootHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsedUrl = urlparse(self.path)
        if parsedUrl.path == '/get':
            params = parse_qs(unquote(parsedUrl.query))

            word = params.get('word', [''])[0]
            pinyin = params.get('pinyin', [''])[0]
            if not word:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("URL param 'word' must be set", 'utf-8'))

            data = generateYomiChanJson(word, pinyin)
            print(data)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data, ensure_ascii=False), 'utf-8'))
        elif parsedUrl.path.startswith('/mp3/'):
            path = unquote(parsedUrl.path[1:])
            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'audio/mpeg')
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                print(path)
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes(f"Failed to find file at: {path}", 'utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(f"Unknown endpoint: {parsedUrl.path}", 'utf-8'))


def runServer():
    port = 8888
    server_address = ('', port)
    httpd = HTTPServer(server_address, RootHandler)
    print(f'Starting httpd on http://localhost:{port}\nUse like this:\nhttp://localhost:8888/get?word=%E9%80%9A%E8%B4%A7%E8%86%A8%E8%83%80&pinyin=t%C5%8Dng%20hu%C3%B2%20p%C3%A9ng%20zh%C3%A0ng')
    httpd.serve_forever()


def synthesizeMp3File(word, pinyin, mp3Path):
    speech_key = loadApiKey()
    service_region = "germanywestcentral"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = "zh-CN"
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    audio_output_config = speechsdk.audio.AudioOutputConfig(filename=str(mp3Path))
    # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)  # FOR DEBUG, will play the audio additionally
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

    if pinyin:
        result = speech_synthesizer.speak_text_async(pinyin).get()
    else:
        result = speech_synthesizer.speak_text_async(word).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        with open(str(mp3Path), "wb") as audio:
            audio.write(result.audio_data)
            print(f"{word} written to {mp3Path}")

    elif result.reason == speechsdk.ResultReason.Canceled:
        if mp3Path.exists():
            mp3Path.unlink()
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        exit(1)


def voiceDemo():
    """
    There are demos of the voices in the 'Speech Studio' where your service is
    Maybe here: https://speech.microsoft.com/portal/291e8d14e04944b7a4a4289dab276a45/voicegallery
    """
    speech_key = loadApiKey()
    service_region = "germanywestcentral"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_language = "zh-CN"
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    word = "目光呆滞"
    speech_synthesizer.speak_text_async(word).get()


def createFilePath(word: str) -> Path:
    mp3Dir = Path(f"./mp3/{datetime.now().strftime('%Y-%m-%d')}")
    if not os.path.exists(mp3Dir):
        os.makedirs(mp3Dir)

    return mp3Dir.joinpath(f"{word}.mp3")


def loadApiKey() -> str:
    apiKeyPath = "./azureApiKey"
    return FileUtils.loadFileAsString(Path(apiKeyPath), f"Failed to load {apiKeyPath}").strip()


def generateYomiChanJson(word: str, pinyin) -> dict:
    word = word.strip()
    path = createFilePath(word)

    if path.exists():
        print(f"{path} already exists")
    else:
        synthesizeMp3File(word, pinyin, path)

    return {
        "type": "audioSourceList",
        "audioSources": [{
            "name": word,
            "url": f"http://localhost:8888/{str(path)}"
        }]
    }
