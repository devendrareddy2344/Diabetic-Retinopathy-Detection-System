# ================================
# DIABETIC RETINOPATHY TRAINING
# EfficientNetB3 + Balanced Data
# ================================

import os
import cv2
import random
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.applications import EfficientNetB3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, cohen_kappa_score

# -------- 1. CONFIG --------
IMG_SIZE = 300
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 1e-4
NUM_CLASSES = 5
SAMPLES_PER_CLASS = 1000

DATA_DIR = r"C:\Users\Krishna\Desktop\Diabetic Retinopathy Detection System\final_dataset\train"

CLASS_MAP = {
    "No_DR": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
    "Proliferative_DR": 4
}

# -------- 2. LOAD & BALANCE DATA --------
def load_and_balance_data(data_dir, samples_per_class):
    print("\n--- Loading & Balancing Dataset ---")
    image_paths, labels = [], []

    for class_name, label in CLASS_MAP.items():
        folder = os.path.join(data_dir, class_name)
        images = [os.path.join(folder, f) for f in os.listdir(folder)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        count = len(images)

        if count >= samples_per_class:
            selected = random.sample(images, samples_per_class)
            print(f"{class_name}: {count} → Undersampled to {samples_per_class}")
        else:
            selected = images * (samples_per_class // count) + random.sample(images, samples_per_class % count)
            print(f"{class_name}: {count} → Oversampled to {samples_per_class}")

        image_paths.extend(selected)
        labels.extend([label] * samples_per_class)

    combined = list(zip(image_paths, labels))
    random.shuffle(combined)
    paths, labels = zip(*combined)

    return np.array(paths), np.array(labels)

# -------- 3. PREPROCESSING --------
def preprocess_image(path):
    img = cv2.imread(path)
    if img is None:
        return np.zeros((IMG_SIZE, IMG_SIZE, 3))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.addWeighted(img, 4, cv2.GaussianBlur(img, (0,0), 10), -4, 128)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    return img.astype(np.float32) / 255.0

# -------- 4. DATA GENERATOR --------
class DRDataGenerator(tf.keras.utils.Sequence):
    def __init__(self, paths, labels, batch_size=32, shuffle=True):
        self.paths = paths
        self.labels = labels
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indexes = np.arange(len(self.paths))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.paths) / self.batch_size))

    def __getitem__(self, idx):
        indexes = self.indexes[idx*self.batch_size:(idx+1)*self.batch_size]
        batch_paths = [self.paths[i] for i in indexes]
        batch_labels = [self.labels[i] for i in indexes]

        X = np.array([preprocess_image(p) for p in batch_paths])
        y = tf.keras.utils.to_categorical(batch_labels, NUM_CLASSES)
        return X, y

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexes)

# -------- 5. LOAD DATA --------
paths, labels = load_and_balance_data(DATA_DIR, SAMPLES_PER_CLASS)

X_train, X_test, y_train, y_test = train_test_split(paths, labels, test_size=0.2, stratify=labels, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.125, stratify=y_train, random_state=42)

print(f"\nTrain: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

train_gen = DRDataGenerator(X_train, y_train, BATCH_SIZE)
val_gen = DRDataGenerator(X_val, y_val, BATCH_SIZE)
test_gen = DRDataGenerator(X_test, y_test, BATCH_SIZE, shuffle=False)

# -------- 6. BUILD MODEL --------
print("\n--- Building EfficientNetB3 ---")
base_model = EfficientNetB3(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

for layer in base_model.layers[:-30]:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.4)(x)
output = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=[
        'accuracy',
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall'),
        tf.keras.metrics.AUC(name='auc_roc'),
        tf.keras.metrics.AUC(name='auc_pr', curve='PR')
    ]
)

# -------- 7. TRAINING --------
callbacks = [
    EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2),
    ModelCheckpoint("best_dr_model_effnet.keras", save_best_only=True, monitor='val_accuracy')
]

print("\n--- Training Model ---")
history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=callbacks)

# -------- 8. EVALUATION --------
print("\n--- Evaluating Model ---")
y_pred_prob = model.predict(test_gen)
y_pred = np.argmax(y_pred_prob, axis=1)
y_true = y_test[:len(y_pred)]

print("\nClassification Report:")
print(classification_report(y_true, y_pred, target_names=CLASS_MAP.keys()))

print("\nQuadratic Weighted Kappa:", cohen_kappa_score(y_true, y_pred, weights='quadratic'))

# -------- 9. SAVE FINAL MODEL --------
model.save("final_dr_model_effnet.keras")
print("\nModel saved as 'final_dr_model_effnet.keras'")

# -------- 10. LEARNING CURVES --------
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend(); plt.title("Accuracy Curve"); plt.show()

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend(); plt.title("Loss Curve"); plt.show()
