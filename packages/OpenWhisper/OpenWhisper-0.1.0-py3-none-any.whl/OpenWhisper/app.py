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
    LOCAL_URL = "http://127.0.0.1:1945/audio/transcriptions"
    REMOTE_URL = "https://whisper.jsdelivr.web.id/audio/transcriptions"

    @staticmethod
    def get_base_url():
        try:
            response = requests.get(Whisper.LOCAL_URL, timeout=2)
            if response.status_code == 200:
                return Whisper.LOCAL_URL
        except requests.exceptions.RequestException:
            pass
        try:
            response = requests.get(Whisper.REMOTE_URL, timeout=2)
            if response.status_code == 200:
                return Whisper.REMOTE_URL
        except requests.exceptions.RequestException:
            pass
        raise ConnectionError("A server error occurred. Please try again later.")

    class Audio:
        class Transcriptions:
            @staticmethod
            def create(file, model, response_format=None, url_base=None):
                if not model:
                    raise ValueError("The 'model' parameter is required.")
                if not url_base:
                    try:
                        url_base = Whisper.get_base_url()
                    except ConnectionError as ce:
                        raise ConnectionError(str(ce))
                with open(file, "rb") as audio_file:
                    headers = {"model": model}
                    if response_format == "text":
                        headers["Accept"] = "text/plain"
                    else:
                        headers["Accept"] = "application/json"
                    files = {"file": audio_file}
                    try:
                        response = requests.post(
                            url_base,
                            headers=headers,
                            files=files,
                        )
                        response.raise_for_status()
                        is_json = headers["Accept"] == "application/json"
                        if is_json:
                            return TranscriptionResponse(response.json(), is_json=True)
                        return TranscriptionResponse(response.text, is_json=False)
                    except requests.exceptions.RequestException:
                        raise RuntimeError("A server error occurred. Please try again later.")

    def __init__(self):
        self.audio = self.Audio()
        self.audio.transcriptions = self.Audio.Transcriptions()