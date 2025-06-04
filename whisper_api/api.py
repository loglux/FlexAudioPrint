from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import whisper
import uvicorn
import os
import tempfile

app = FastAPI()

# Cache for loaded models
model_cache = {}
current_model_name = None

def get_model(model_name):
    global current_model_name
    if model_name not in model_cache:
        print(f"==> LOADING NEW MODEL: {model_name}")
        try:
            model_cache[model_name] = whisper.load_model(model_name)
        except Exception as e:
            print(f"ERROR: Failed to load model {model_name}: {e}")
            return None
    else:
        print(f"==> USING CACHED MODEL: {model_name}")
    current_model_name = model_name
    return model_cache.get(model_name)

@app.post("/transcribe/")
async def transcribe(
    audio: UploadFile = File(...),
    initial_prompt: str = Form(None),
    task: str = Form("transcribe"),
    model_name: str = Form("turbo"),
):
    print(f"==> MODEL NAME RECEIVED: {model_name}")
    suffix = os.path.splitext(audio.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await audio.read())
        temp_audio_path = temp_audio.name

    model = get_model(model_name)
    if model is None:
        os.remove(temp_audio_path)
        return JSONResponse(content={"error": f"Model {model_name} failed to load."}, status_code=500)
    result = model.transcribe(temp_audio_path, initial_prompt=initial_prompt, task=task)
    os.remove(temp_audio_path)
    return JSONResponse(content={"text": result["text"], "segments": result["segments"]})

@app.get("/")
def root():
    # Always return status and current model name (even if not loaded yet)
    return {
        "status": "ok",
        "current_model": current_model_name
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9911)
