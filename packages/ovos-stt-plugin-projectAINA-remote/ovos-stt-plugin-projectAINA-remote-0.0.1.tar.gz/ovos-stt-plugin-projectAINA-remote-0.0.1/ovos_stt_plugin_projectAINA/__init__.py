from typing import Optional

import requests
from ovos_plugin_manager.templates.stt import STT
from ovos_utils.log import LOG
from speech_recognition import AudioData


class ProjectAINARemoteSTT(STT):
    SERVERS = [
        "https://h3xisjmpemyv68l1.us-east-1.aws.endpoints.huggingface.cloud",  # citrinet
        "https://zl8yec0awthroezf.eu-west-1.aws.endpoints.huggingface.cloud"  # whisper
    ]

    def __init__(self, config: dict = None):
        super().__init__(config)
        self.token = self.config.get("hf_token")
        if not self.token:
            raise ValueError("hf_token is required!")

    def execute(self, audio: AudioData, language: Optional[str] = None):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "audio/wav"
        }
        data = audio.get_wav_data()
        for url in self.SERVERS:
            try:
                response = requests.post(url, headers=headers, data=data).json()
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response["text"]
            except Exception as e:
                LOG.error(f"Server {url} failed: {e}")
                continue
        raise RuntimeError("Failed to reach Project AINA servers")

    @property
    def available_languages(self) -> set:
        return {"ca"}


if __name__ == "__main__":
    b = ProjectAINARemoteSTT(config={"hf_token": "hf_....."})
    from speech_recognition import Recognizer, AudioFile

    ca = "/home/miro/PycharmProjects/ovos-stt-plugin-vosk/example.wav"
    with AudioFile(ca) as source:
        audio = Recognizer().record(source)

    a = b.execute(audio, language="ca")
    print(a)
