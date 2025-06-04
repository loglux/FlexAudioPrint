# whisper_api.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import whisper
import uvicorn
import os
import tempfile

model = whisper.load_model("base")  # или любой нужный

app = FastAPI()

@app.post("/transcribe/")
async def transcribe(audio: UploadFile, initial_prompt: str = Form(None), task: str = Form("transcribe")):
    # Saving a temporary file
    suffix = os.path.splitext(audio.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await audio.read())
        temp_audio_path = temp_audio.name

    # Transcribing
    result = model.transcribe(temp_audio_path, initial_prompt=initial_prompt, task=task)
    os.remove(temp_audio_path)
    return JSONResponse(content={"text": result["text"], "segments": result["segments"]})


@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    # in the console to start:
    uvicorn.run(app, host="0.0.0.0", port=90911)
