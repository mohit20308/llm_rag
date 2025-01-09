import base64
import os

import requests
from dotenv import load_dotenv


class TranslateTTS:
    def __init__(self):
        load_dotenv('.env')
        self.translate_url = "https://api.sarvam.ai/translate"
        self.tts_url = "https://api.sarvam.ai/text-to-speech"
        self.headers = {
            "api-subscription-key": os.getenv('SARVAM_API_KEY'),
            "Content-Type": "application/json"
        }

    def translate_text(self, input_text):
        '''Take text as input in english language and return the text in hindi language (Translation)'''
        payload = {
            "input": input_text,
            "source_language_code": "en-IN",
            "target_language_code": "hi-IN",
            "speaker_gender": "Female",
            "mode": "formal",
            "model": "mayura:v1",
            "enable_preprocessing": True
        }

        response = requests.request("POST", self.translate_url, json = payload, headers = self.headers)
        if response.status_code == 200:
            translated_text = response.json()['translated_text']
            return translated_text

        elif 400 <= response.status_code <= 500:
            error = response.json()['error']
            return error['message']

    def tts(self, translated_text):
        '''Take text as input in hindi language and create a .wav file and returns a message (Text to Speech)'''
        payload = {
            "inputs": [translated_text],
            "target_language_code": "hi-IN",
            "speaker": "meera",
            "model": "bulbul:v1",
            "enable_preprocessing": True,
            "speech_sample_rate": 16000,
            "loudness": 2,
            "pitch": 0,
            "pace": 1.2
        }

        response = requests.request("POST", self.tts_url, json = payload, headers = self.headers)
        if response.status_code == 200:
            encoded_audio = response.json()['audios'][0]
            decoded_audio = base64.b64decode(encoded_audio)
            with open('output.wav', 'wb') as fhandle:
                fhandle.write(decoded_audio)
            return "File Created"

        elif 400 <= response.status_code <= 500:
            error = response.json()['error']
            return error['message']