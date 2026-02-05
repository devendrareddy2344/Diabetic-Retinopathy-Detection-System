import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Force CPU (Render has no GPU)

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import preprocess_image

app = FastAPI(
    title="Diabetic Retinopathy Detection API",
    description="AI system for retinal disease grading using InceptionV3",
    version="3.0"
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Path to your trained Inception model
MODEL_PATH = os.path.join("app", "models", "final_dr_model_inception.keras")
model = None

# Class labels (must match CLASS_MAP order)
CLASSES = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR"
}

# 🔹 Load model at server startup
@app.on_event("startup")
def load_model():
    global model
    try:
        print("Loading InceptionV3 DR model...")
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

        # Preprocess image (must match training)
        img = preprocess_image(contents)

        # Model prediction
        preds = model.predict(img)
        class_idx = int(np.argmax(preds[0]))
        confidence = float(np.max(preds[0]))

        return {
            "diagnosis": CLASSES[class_idx],
            "severity_grade": class_idx,
            "confidence": round(confidence * 100, 2),
            "raw_probabilities": preds[0].tolist()
        }

    except Exception as e:
        print(" Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))
