import cv2
import numpy as np

IMG_SIZE = 300  # MUST match training

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Ben Graham preprocessing (same as training)
    img = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0,0), 10), -4, 128)

    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0

    return np.expand_dims(img, axis=0)  # Shape: (1, 300, 300, 3)
