import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU (Render uses CPU)

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import preprocess_image

app = FastAPI(
    title="Diabetic Retinopathy Detection API",
    description="AI system for retinal disease grading using EfficientNetB3",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Use absolute path (important on Render)
MODEL_PATH = os.path.join("app", "models", "final_dr_model_effnet.keras")
model = None

CLASSES = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR"
}

# 🔹 Load model once at startup
@app.on_event("startup")
def load_model():
    global model
    try:
        print(" Loading EfficientNetB3 model...")
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print(" Model loaded successfully!")
    except Exception as e:
        print(f" Model loading failed: {e}")

@app.get("/")
def home():
    return {"status": "online", "message": "DR Detection API Ready"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        contents = await file.read()

        # Preprocess must match training IMG_SIZE
        img = preprocess_image(contents)

        preds = model.predict(img)
        class_idx = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))

        return {
            "diagnosis": CLASSES[class_idx],
            "severity_grade": class_idx,
            "confidence": round(confidence * 100, 2)
        }

    except Exception as e:
        print(" Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))
