import requests


class TranscriptionResponse:
    def __init__(self, response, is_json):
        if is_json:
            self.text = response.get("text", "")
            self.raw = response
        else:
            self.text = response
            self.raw = {"text": response}

    def __getitem__(self, key):
        return self.raw[key]


class Whisper:
    DEFAULT_API_URL = "https://whisperv3.jsdelivr.web.id/audio/transcriptions"

    class Audio:
        class Transcriptions:
            @staticmethod
            def create(file, model="whisper-v3-turbo", response_format=None, api_url=None):
                if not api_url:
                    api_url = Whisper.DEFAULT_API_URL
                with open(file, "rb") as audio_file:
                    headers = {"model": model}
                    if response_format == "text":
                        headers["Accept"] = "text/plain"
                    else:
                        headers["Accept"] = "application/json"
                    files = {"file": audio_file}
                    response = requests.post(
                        api_url,
                        headers=headers,
                        files=files,
                    )
                    response.raise_for_status()
                    is_json = headers["Accept"] == "application/json"
                    if is_json:
                        return TranscriptionResponse(response.json(), is_json=True)
                    return TranscriptionResponse(response.text, is_json=False)

    def __init__(self):
        self.audio = self.Audio()
        self.audio.transcriptions = self.Audio.Transcriptions()
