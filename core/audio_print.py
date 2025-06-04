import subprocess
import whisper
import os

class AudioTranscriber:
    def __init__(self, model_name="base"):
        print(f"Loading model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print(f"Model {model_name} loaded successfully.")

    def transcribe_audio(self, audio_path, initial_prompt=None, task="transcribe"):
        """
        Transcribes text from an audio file.
        :param audio_path: Path to the audio file
        :return: Dictionary with transcribed text and segments
        """
        print(f"Transcribing text from the file {audio_path}...")
        print(f"initial_prompt: {initial_prompt}...")
        print(f"task: {task}...")
        result = self.model.transcribe(audio_path, initial_prompt=initial_prompt, task=task)
        print("Transcription completed.")
        print(result)

        return {
            "text": result["text"],  # Full transcription text
            "segments": result["segments"]  # Segments with timestamps for subtitles
        }

    def process_audio(self, input_path, initial_prompt=None, output_text_path=None, task="transcribe"):
        """
        Complete processing cycle for an audio file: transcription.
        :param input_path: Path to the input audio file
        :param initial_prompt: Optional initial prompt for the transcription
        :param output_text_path: Path to save the transcribed text
        :return: Transcribed text
        """
        # Speech recognition
        text = self.transcribe_audio(input_path, initial_prompt, task=task)

        # Save text to a file if a path is specified
        if output_text_path:
            with open(output_text_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Transcribed text has been saved to the file {output_text_path}")
        return text

if __name__ == "__main__":
    # Path to your audio file
    input_audio = "first.mp3"

    # Path for saving the text
    output_text_file = "../recognized_text.txt"

    # Creating an instance of the class
    audio_transcriber = AudioTranscriber('large')

    # Recognising the text and saving it to a file
    result = audio_transcriber.process_audio(input_audio, output_text_path=output_text_file)
    print("Recognised text:")
    print(result)


