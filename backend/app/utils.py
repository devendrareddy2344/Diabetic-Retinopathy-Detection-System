import cv2
import numpy as np

# InceptionV3 input size
IMG_SIZE = 299  

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess retinal image exactly like training pipeline.
    """

    # Convert bytes → numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image")

    # Convert BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Ben Graham contrast normalization
    img = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0, 0), 10), -4, 128)

    # Resize to InceptionV3 input size
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # Normalize pixel values
    img = img.astype(np.float32) / 255.0

    # Add batch dimension → (1, 299, 299, 3)
    return np.expand_dims(img, axis=0)
