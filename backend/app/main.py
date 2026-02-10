import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.utils import preprocess_image

app = FastAPI(
    title="Diabetic Retinopathy Detection API",
    description="AI system for retinal disease grading using InceptionV3 (TFLite)",
    version="4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Path to your TFLite model
MODEL_PATH = os.path.join("app", "models", "dr_model_compressed.tflite")

# TFLite Interpreter variables
interpreter = None
input_details = None
output_details = None

CLASSES = {
    0: "No DR",
    1: "Mild",
    2: "Moderate",
    3: "Severe",
    4: "Proliferative DR"
}

# 🔹 Load TFLite model at startup
@app.on_event("startup")
def load_model():
    global interpreter, input_details, output_details
    try:
        print(" Loading TFLite DR model...")
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        print(" TFLite model loaded successfully!")
    except Exception as e:
        print(f" Model loading failed: {e}")


@app.get("/")
def home():
    return {"status": "online", "message": "DR Detection API Ready (TFLite)"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    if interpreter is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        contents = await file.read()

        # Preprocess image → shape (1, 299, 299, 3)
        img = preprocess_image(contents)

        # Ensure dtype matches model input (usually float32)
        img = img.astype(input_details[0]['dtype'])

        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], img)

        # Run inference
        interpreter.invoke()

        # Get output tensor
        preds = interpreter.get_tensor(output_details[0]['index'])[0]

        class_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))

        return {
            "diagnosis": CLASSES[class_idx],
            "severity_grade": class_idx,
            "confidence": round(confidence * 100, 2),
            "raw_probabilities": preds.tolist()
        }

    except Exception as e:
        print(" Prediction error:", e)
        raise HTTPException(status_code=500, detail=str(e))
