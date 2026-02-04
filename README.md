# 👁️ Diabetic Retinopathy AI Detection System

An end-to-end Deep Learning application designed to detect and grade Diabetic Retinopathy (DR) from retinal fundus images. This system leverages a fine-tuned **EfficientNet-B3** model, served via a high-performance **FastAPI** backend, and accessible through a modern **React + TypeScript** frontend.

## 🚀 Features

* **AI-Powered Diagnosis:** Automatically classifies retinal images into 5 severity stages:
    * 0 - No DR
    * 1 - Mild
    * 2 - Moderate
    * 3 - Severe
    * 4 - Proliferative DR
* **Advanced Preprocessing:** Implements **Ben Graham’s method** (Local Gaussian Blur subtraction) to normalize lighting and enhance lesion visibility.
* **High Accuracy:** Uses **EfficientNet-B3** with Transfer Learning, optimized for medical imaging at **300x300** resolution.
* **Smart Data Balancing:** Custom training pipeline that balances the dataset to **1200 samples per class** to prevent bias towards the majority class.
* **Interactive UI:** Modern React interface with drag-and-drop upload, instant visual feedback, and clear severity grading.

---

## 🛠️ Tech Stack

### **Frontend**
* **Framework:** React 18 + TypeScript
* **Build Tool:** Vite
* **Styling:** Tailwind CSS
* **State Management:** React Hooks
* **API Client:** Axios

### **Backend**
* **Framework:** FastAPI
* **ML Engine:** TensorFlow / Keras
* **Image Processing:** OpenCV (cv2), NumPy
* **Server:** Uvicorn (ASGI)

### **Machine Learning**
* **Model:** EfficientNet-B3
* **Input Resolution:** 300x300 pixels
* **Training Strategy:** Transfer Learning (ImageNet weights) + Fine-Tuning

---

## 📂 Project Structure

```text
diabetic-retinopathy-system/
│
├── backend/                  # [Server] FastAPI Application
│   ├── app/
│   │   ├── models/           # Stores the trained .keras/.h5 model
│   │   ├── main.py           # API Endpoints (Upload & Predict)
│   │   └── utils.py          # Image preprocessing logic (Ben Graham)
│   ├── requirements.txt      # Python dependencies
│   └── Procfile              # Render deployment config
│
├── frontend/                 # [Client] React Application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   └── App.tsx           # Main application logic
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Styling configuration
│   ├── vite.config.ts        # Build configuration
│   └── vercel.json           # Vercel deployment config
│
├── training/                 # [AI] Model Development
│   ├── train_dr_efficientnet.py   # Main training script
│   └── requirements.txt
│
└── README.md                 # Project Documentation