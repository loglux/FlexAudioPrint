import gradio as gr
from audio_print import AudioTranscriber

# Creating an instance of AudioTranscriber
audio_transcriber = AudioTranscriber('large')


def transcribe_audio(audio_file):
    try:
        return audio_transcriber.process_audio(audio_file)
    except Exception as e:
        return f"Ошибка: {str(e)}"


def save_text_to_file(text):
    try:
        file_path = "output.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        return file_path  # Return file path for download
    except Exception as e:
        return None  # Return None in case of an error

def _save_text_to_file(text):
    try:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return "Text successfully saved in output.txt"
    except Exception as e:
        return f"Error while saving: {str(e)}"


# Настройка интерфейса
with gr.Blocks() as demo:
    gr.Markdown("# Audio Recognition")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload an audio file")
    transcribe_button = gr.Button("Transcribe")

    with gr.Row():
        text_output = gr.Textbox(label="Recognized Text", lines=5)

    gr.Markdown("### Save the Result (press the Save button to get the file)")
    with gr.Row():
        with gr.Column():
            save_button = gr.Button("Save")
        with gr.Column():
            download_button = gr.File(label="Download the file")

    # Button bindings to functions
    transcribe_button.click(transcribe_audio, inputs=audio_input, outputs=text_output)
    save_button.click(save_text_to_file, inputs=text_output,
                      outputs=download_button)  # Save and provide file to download

# Launch the application
demo.launch()
