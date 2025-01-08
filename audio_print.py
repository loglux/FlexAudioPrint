import subprocess
import whisper
import os

class AudioTranscriber:
    def __init__(self, model_name="base"):
        print(f"Loading model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print(f"Model {model_name} loaded successfully.")

    def convert_audio(self, input_path, output_path):
        """
        Converts an audio file to the WAV format with parameters of 16kHz sampling rate and mono channel for compatibility with the Whisper model.
        :param input_path: Path to the input audio file
        :param output_path: Path to save the converted audio file
        """
        print(f"Converting file {input_path} to {output_path}...")
        subprocess.run([
            "ffmpeg", "-i", input_path, "-ar", "16000", "-ac", "1", "-y", output_path
        ], check=True)
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"File {output_path} hasn't been created.")
        print(f"File {output_path} created successfully.")

    def transcribe_audio(self, audio_path):
        """
        Transcribes text from an audio file.
        :param audio_path: Path to the audio file
        :return: Transcribed text
        """
        print(f"Transcribing text from the file {audio_path}...")
        result = self.model.transcribe(audio_path)
        print("Transcription completed.")

        return result["text"]

    def process_audio(self, input_path, output_text_path=None):
        """
        Complete processing cycle for an audio file: conversion and transcription.
        :param input_path: Path to the input audio file
        :param output_text_path: Path to save the transcribed text
        :return: Transcribed text
        """
        temp_path = "temp_audio.wav"
        try:
            # Audio file conversion
            self.convert_audio(input_path, temp_path)

            # Speech recognition
            text = self.transcribe_audio(temp_path)

            # Save text to a file if a path is specified
            if output_text_path:
                with open(output_text_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Transcribed text has been saved to the file {output_text_path}")
            return text
        finally:
            # Deleting the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                print(f"The temporary file {temp_path} has been deleted.")

if __name__ == "__main__":
    # Path to your audio file
    input_audio = "rus_test.wav"

    # Path for saving the text
    output_text_file = "recognized_text.txt"

    # Creating an instance of the class
    audio_transcriber = AudioTranscriber('large')

    # Recognising the text and saving it to a file
    result_text = audio_transcriber.process_audio(input_audio, output_text_path=output_text_file)
    print("Recognised text:")
    print(result_text)


