# 👁️ Diabetic Retinopathy AI Detection System

An end-to-end Deep Learning application designed to detect and grade Diabetic Retinopathy (DR) from retinal fundus images. This system leverages a fine-tuned **InceptionV3** model, served via a high-performance **FastAPI** backend, and accessible through a modern **React + TypeScript** frontend.

## 🚀 Features

### 🧠 AI-Powered Diagnosis
Automatically classifies retinal images into 5 severity stages:

| Grade | Diagnosis |
| :---: | :--- |
| **0** | No DR |
| **1** | Mild |
| **2** | Moderate |
| **3** | Severe |
| **4** | Proliferative DR |

### 🔬 Advanced Medical Image Preprocessing
Implements **Ben Graham’s method** (Local Gaussian Blur subtraction) to normalize uneven lighting, enhance blood vessels, and improve lesion visibility, matching clinical DR research standards.

### 🏆 High-Performance Deep Learning Model
* **Model Architecture:** InceptionV3
* **Input Resolution:** 299 × 299 pixels
* **Training Strategy:** Transfer Learning (ImageNet) + Fine-Tuning
* **Loss Function:** Categorical Crossentropy
* **Evaluation Metric:** Quadratic Weighted Kappa (medical grading standard)

### ⚖️ Smart Data Balancing
Custom training pipeline balances the dataset to equal samples per class, reducing bias toward "No DR" cases and improving multi-class detection performance.

### 💻 Interactive User Interface
* Drag-and-drop retinal image upload
* Instant AI analysis
* Clear severity grading display
* Confidence score for each prediction

## 🛠️ Tech Stack

### Frontend
* **Framework:** React 18 + TypeScript
* **Build Tool:** Vite
* **Styling:** Tailwind CSS
* **State Management:** React Hooks
* **API Client:** Axios

### Backend
* **Framework:** FastAPI
* **ML Engine:** TensorFlow / Keras
* **Image Processing:** OpenCV (cv2), NumPy
* **Server:** Uvicorn (ASGI)

### Machine Learning Details
| Component | Details |
| :--- | :--- |
| **Model** | InceptionV3 |
| **Input Size** | 299 × 299 |
| **Classes** | 5 DR severity levels |
| **Output** | Softmax probabilities |
| **Optimization** | Adam Optimizer |
| **Learning Rate** | Low LR for fine-tuning |
| **Preprocessing** | Ben Graham normalization |

## 📂 Project Structure

```text
diabetic-retinopathy-system/
│
├── backend/                  # [Server] FastAPI Application
│   ├── app/
│   │   ├── models/           # Stores trained model (.keras)
│   │   ├── main.py           # API Endpoints (Upload & Predict)
│   │   └── utils.py          # Image preprocessing (Ben Graham)
│   ├── requirements.txt      # Python dependencies
│   └── Procfile              # Render deployment config
│
├── frontend/                 # [Client] React Application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   └── App.tsx           # Main app logic
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── vercel.json           # Vercel deployment config
│
├── training/                 # [AI] Model Development
│   ├── InceptionV3.ipynb     # Final training notebook
│   └── requirements.txt
│
└── README.md                 # Project Documentation