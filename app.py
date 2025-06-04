import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv("USE_REMOTE_API", "false").lower() == "true":
    from core.audio_print_api import AudioTranscriber
else:
    from core.audio_print import AudioTranscriber
from core.transcript_formatter import TranscriptFormatter
import gradio as gr


class AudioProcessor:
    def __init__(self, default_model='turbo'):
        self.audio_transcriber = AudioTranscriber(default_model)
        self.current_model = default_model
        self.transcript_formatter = TranscriptFormatter()
        self.last_transcript_path = None

    def set_model(self, model_name):
        """Set a new model for transcription."""
        if model_name != self.current_model:
            self.audio_transcriber = AudioTranscriber(model_name)
            self.current_model = model_name
        return f"Model set to: {model_name}"

    def reset_model(self):
        """Reset the model to the default if necessary."""
        if self.current_model != 'turbo':  # Checking the current model
            self.audio_transcriber = AudioTranscriber('turbo')
            self.current_model = 'turbo'
        return f"Model set to: {self.current_model}"  # Returning the current state

    def _get_base_name(self, file_path):
        """Returns the base name of a file without the extension."""
        original_filename = os.path.basename(file_path)
        base_name, _ = os.path.splitext(original_filename)
        return base_name

    def _toggle_translate_button(model_name):
        # Возвращаем обновление компонента с видимостью
        if model_name in ["medium", "large", "small", "base"]:
            return gr.update(visible=True)
        else:
            return gr.update(visible=False)

    @staticmethod
    def toggle_translate_button(model_name):
        return gr.update(visible=model_name in ["medium", "large", "small", "base"])

    def transcribe_audio(self, audio_file, initial_prompt, model_name, task="transcribe"):
        try:
            self.set_model(model_name)

            # Extract the original file name and its base name without the extension
            base_name = self._get_base_name(audio_file)

            # Transcription of an audio file
            result = self.audio_transcriber.process_audio(audio_file, initial_prompt, task=task)
            transcribed_text = result["text"]

            # Path for saving the text file with the original name
            text_file_path = f"{base_name}.txt"

            # Save the transcript to a text file
            with open(text_file_path, mode="w", encoding="utf-8") as text_file:
                text_file.write(transcribed_text)

            self.last_transcript_path = text_file_path # remember the path

            return transcribed_text, result, text_file_path
        except Exception as e:
            return f"Error: {str(e)}", None, None


    def generate_srt(self, result, audio_file):
        try:
            # Extract the base name of the audio file
            base_name = self._get_base_name(audio_file)

            # Path for saving the SRT file
            srt_file_path = f"{base_name}.srt"

            # Save segments to an SRT file
            with open(srt_file_path, mode="w", encoding="utf-8") as srt_file:
                for i, segment in enumerate(result["segments"]):
                    start = self.format_time(segment["start"])
                    end = self.format_time(segment["end"])
                    text = segment["text"].strip()
                    srt_file.write(f"{i + 1}\n{start} --> {end}\n{text}\n\n")

            return srt_file_path
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def format_time(seconds):
        millis = int((seconds % 1) * 1000)
        seconds = int(seconds)
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"

    def format_transcript(self, raw_text):
        formatted = self.transcript_formatter.format_transcript(raw_text)

        if self.last_transcript_path:
            base_name, _ = os.path.splitext(self.last_transcript_path)
            output_path = f"{base_name}_formatted.txt"
        else:
            output_path = "formatted_output.txt"

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(formatted)
        except Exception as e:
            print(f"Error saving file: {e}")
            return formatted, None

        return formatted, output_path


# Initialize processor with default model
audio_processor = AudioProcessor(default_model='turbo')

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Audio Recognition and Subtitle Generator")

    with gr.Row():
        with gr.Column(scale=1):
            model_selector = gr.Dropdown(
                label="Select Model",
                choices=["tiny", "base", "small", "medium", "large", "turbo"],
                value="turbo",
                interactive=True
            )

        with gr.Column(scale=1):
            model_status = gr.Textbox(
                label="Current Model",
                value="Model set to: turbo",
                interactive=False
           )

    with gr.Row():
        with gr.Column(scale=1):
            set_model_button = gr.Button("Set Model")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload an audio file")

    with gr.Row():
        gr.Markdown(
            """
            **What is a Hint (Prompt)?**

            The "Hint" is an optional brief prompt you can provide about the content of the audio file.
            **Do not overload it with unnecessary details.**

            - For example, instead of:
              `This is a detailed discussion about Kubernetes, Docker, microservices, and CI/CD pipelines.`
            - it's better to say:
              `Kubernetes, Docker, microservices, CI/CD pipelines`.
            """
        )


    with gr.Row():
        initial_prompt = gr.Textbox(label="Hint (Optional) ", placeholder="Hint about the content of the audio file")

    with gr.Row():
        transcribe_button = gr.Button("Transcribe")
        translate_button = gr.Button("Translate", visible=False)

    with gr.Row():
        text_output = gr.Textbox(label="Recognized Text", lines=5)
        download_text_button = gr.File(label="Download Transcribed Text")

    with gr.Row():
        format_button = gr.Button("Format Transcript")

    with gr.Row():
        formatted_output = gr.Textbox(label="Formatted Transcript", lines=10)
        save_formatted_button = gr.File(label="Download Formatted Text")

    gr.Markdown("### Generate Subtitles")
    with gr.Row():
        generate_srt_button = gr.Button("Generate SRT")
        download_srt_button = gr.File(label="Download SRT Subtitles")

    transcription_state = gr.State()

    set_model_button.click(
        fn=audio_processor.set_model,
        inputs=[model_selector],
        outputs=[model_status]
    )

    set_model_button.click(
        fn=AudioProcessor.toggle_translate_button,  # Статический метод
        inputs=[model_selector],
        outputs=[translate_button]  # Обновляем сам компонент, а не его атрибут
    )

    transcribe_button.click(
        audio_processor.transcribe_audio,
        inputs=[audio_input, initial_prompt, model_selector],
        outputs=[text_output, transcription_state, download_text_button]
    )

    translate_button.click(
        fn=lambda audio_file, initial_prompt: audio_processor.transcribe_audio(audio_file, initial_prompt,
                                                                               task='translate'),
        inputs=[audio_input, initial_prompt],  # Используем initial_prompt
        outputs=[text_output, transcription_state, download_text_button]
    )

    generate_srt_button.click(
        audio_processor.generate_srt,
        inputs=[transcription_state, audio_input],
        outputs=download_srt_button
    )

    format_button.click(
        fn=audio_processor.format_transcript,
        inputs=[text_output],
        outputs=[formatted_output, save_formatted_button]
    )

    demo.load(
        fn=lambda: (audio_processor.reset_model(), "turbo"),
        inputs=[],
        outputs=[model_status, model_selector]
    )

if __name__ == "__main__":
    demo.launch()
