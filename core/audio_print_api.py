import os
import requests


def remote_transcribe(audio_path, initial_prompt, model_name="turbo", task="transcribe", host="localhost", port=9911):
    """
    Sends an audio file to a remote Whisper API for transcription.
    :param audio_path: Path to the audio file
    :param initial_prompt: Optional initial prompt for transcription
    :param task: Transcription task ("transcribe" or "translate")
    :param host: Host of the remote API
    :param port: Port of the remote API
    :return: JSON response with transcription results
    """
    url = f"http://{host}:{port}/transcribe/"
    with open(audio_path, "rb") as f:
        files = {"audio": (os.path.basename(audio_path), f, "audio/mpeg")}
        data = {"initial_prompt": initial_prompt, "task": task, "model_name": model_name}
        response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    return response.json()


class AudioTranscriber:
    def __init__(self, model_name="turbo", host="localhost", port=9911):
        self.model_name = model_name
        self.host = host
        self.port = port

    def transcribe_audio(self, audio_path, initial_prompt=None, task="transcribe"):
        # Вызывает удалённый сервис для транскрипции
        return remote_transcribe(
            audio_path,
            initial_prompt,
            self.model_name,
            task,
            host=self.host,
            port=self.port
        )

    def process_audio(self, input_path, initial_prompt=None, output_text_path=None, task="transcribe"):
        text = self.transcribe_audio(input_path, initial_prompt, task=task)
        if output_text_path:
            with open(output_text_path, "w", encoding="utf-8") as f:
                f.write(text["text"])
        return text

if __name__ == "__main__":
    # Тестовый запуск
    input_audio = "test.mp3"
    output_text_file = "../recognized_text.txt"
    audio_transcriber = AudioTranscriber(host="192.168.1.100", port=9911)  # Подставьте свой IP/порт!
    result = audio_transcriber.process_audio(input_audio, output_text_path=output_text_file)
    print("Recognised text:")
    print(result)
