# Audio Transcription App

A user-friendly audio transcription web application built using **Gradio** and **OpenAI's Whisper** model. This app allows users to upload audio files, transcribe them to text, and even save the output for later use.

---

## Features
- **Audio Upload**: Upload audio files in various formats.
- **Automatic Formatting**: Converts audio to the WAV format (16kHz, mono) for compatibility with the Whisper model.
- **Accurate Transcription**: Uses OpenAI's **Whisper** model for speech-to-text transcription.
- **Downloadable Results**: Save your transcription as a file and download it with a single click.
- **Intuitive Web UI**: Built using **Gradio** for a smooth and interactive user interface.
- **Direct Programmatic Usage**: Use `audio_print.py` as a standalone utility to transcribe audio files without the GUI.

---

## Requirements

To use the app, ensure the following are installed on your system:
- **Python 3.10+**
- **`ffmpeg`** (cross-platform multimedia framework, required for audio processing)
- Python packages:
  - **Whisper**
  - **Gradio**
  - **FFmpeg-python** (optional, if used)

---

## Installation

### 1. Clone the Repository
Clone this repository to your local system:
```bash
git clone https://github.com/Loglux/FlexAudioPrint.git
cd FlexAudioPrint
```

### 2. Install Python Dependencies
Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Ensure `ffmpeg` is Installed
- For Windows, download `ffmpeg` from [FFmpeg.org](https://ffmpeg.org/download.html) and add it to your system's PATH.
- For Linux/MacOS, install via your package manager:
  ```bash
  sudo apt install ffmpeg   # For Debian/Ubuntu
  brew install ffmpeg       # For Mac using Homebrew
  ```

---

## Usage

### Use with GUI (Gradio)
1. Run the Gradio app:
   ```bash
   python app.py
   ```

2. Open the URL provided by Gradio (e.g., `http://127.0.0.1:7860/`) in your browser and interact with the web interface.

---

### Use `audio_print.py` Without the GUI
To run the transcription process directly from the command line or using Python scripts, you can use `audio_print.py`.

#### Example Command Line Usage
If you have an audio file and want to transcribe its contents without the GUI:
```bash
python audio_print.py
```

Modify the paths in `audio_print.py` (`input_audio` and `output_text_file`) with the file names of your choice for the audio file you'd like to transcribe and the output file to save the transcription.

---

## Folder Structure
Here's how the project is structured:

---

## How It Works

### 1. **Audio File Upload**
Users can upload an audio file in the Gradio UI. Supported formats include `.wav`, `.mp3`, `.aac`, and others.

### 2. **Audio Conversion**
The app converts the uploaded audio to a `.wav` file with a 16kHz sampling rate and mono channel for compatibility with **Whisper**.

### 3. **Transcription**
The `AudioTranscriber` class uses **Whisper**'s speech-to-text model to transcribe the converted audio into text.

### 4. **Output**
The transcribed text is displayed in the Gradio interface, and the user can save it as a file to download.

---

## Example Usage with Code
If you want to test the transcription programmatically, you can use `audio_print.py`:
```python
from audio_print import AudioTranscriber

# Path to your audio file
input_audio = "example_audio.mp3"

# Path for saving the text transcription
output_text_file = "transcription.txt"

# Create an instance of the AudioTranscriber class
audio_transcriber = AudioTranscriber(model_name="base")

# Process the audio file and save the transcription
result = audio_transcriber.process_audio(input_audio, output_text_path=output_text_file)

print("Recognized Text:", result)
```

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this project according to the terms of the license.

---

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for any improvements or bug fixes.

---

## Acknowledgments

- **Gradio**: For building an effortless web UI for machine learning models.
- **OpenAI Whisper**: For the incredible whisper-based speech-to-text transcription model.
- **FFmpeg**: For reliable audio processing and conversion.

