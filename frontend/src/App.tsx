import { useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import ResultCard from './components/ResultCard';

// CONFIGURATION: Backend URL
const API_URL = "http://127.0.0.1:8000/predict"; 

interface PredictionResult {
  diagnosis: string;
  severity_grade: number;
  confidence: number;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Handle when user picks a file
  const handleFileSelection = (selectedFile: File) => {
    setFile(selectedFile);
    setResult(null); // Clear previous results
    setError(null);
    setPreview(URL.createObjectURL(selectedFile)); // Create preview URL
  };

  // Handle removing the file (Resets the UI)
  const handleClearFile = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  // Send to Backend
  const analyzeImage = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setResult(response.data);
      
    } catch (err) {
      console.error("Analysis failed:", err);
      setError("Failed to connect to the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-10 flex flex-col items-center">
        
        <div className="w-full max-w-3xl bg-white p-8 rounded-2xl shadow-xl">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-slate-800">Upload Retinal Scan</h2>
            <p className="text-slate-500 mt-2">
              Our AI analyzes fundus images to detect signs of Diabetic Retinopathy.
            </p>
          </div>

          {/* LOGIC CHANGE: 
            If NO file is selected -> Show the Big Upload Box.
            If YES file is selected -> Show the Preview + Small "Change" button.
          */}
          
          {!file ? (
            // State 1: No File Selected (Show Big Dropzone)
            <FileUpload onFileSelect={handleFileSelection} isLoading={loading} />
          ) : (
            // State 2: File Selected (Show Preview Area)
            <div className="mt-4 flex flex-col items-center animate-fade-in bg-slate-50 p-6 rounded-xl border border-slate-200">
              
              <div className="relative">
                <img 
                  src={preview!} 
                  alt="Preview" 
                  className="w-64 h-64 object-cover rounded-lg shadow-md border-2 border-white"
                />
                
                {/* Small 'X' button to remove image */}
                {!loading && (
                    <button 
                        onClick={handleClearFile}
                        className="absolute -top-3 -right-3 bg-red-500 hover:bg-red-600 text-white rounded-full p-1.5 shadow-lg transition-transform hover:scale-110"
                        title="Remove image"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-4 h-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                )}
              </div>

              <div className="mt-4 flex flex-col items-center gap-2">
                  <p className="text-sm font-semibold text-slate-700">{file.name}</p>
                  {!loading && !result && (
                      <button 
                          onClick={handleClearFile}
                          className="text-xs text-blue-600 hover:text-blue-800 underline font-medium"
                      >
                          Upload a different file
                      </button>
                  )}
              </div>
            </div>
          )}

          {/* Analyze Button */}
          {file && !result && (
            <div className="mt-8 flex justify-center">
              <button
                onClick={analyzeImage}
                disabled={loading}
                className={`
                  px-8 py-3 rounded-full font-bold text-white text-lg shadow-lg transition-transform transform hover:scale-105
                  ${loading 
                    ? "bg-slate-400 cursor-wait scale-100" 
                    : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
                  }
                `}
              >
                {loading ? (
                  <span className="flex items-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  "Run Analysis"
                )}
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 text-red-600 border border-red-200 rounded-lg text-center animate-fade-in">
              {error}
            </div>
          )}

          {/* Results Display */}
          {result && (
            <div className="animate-fade-in">
                <ResultCard 
                diagnosis={result.diagnosis} 
                severity={result.severity_grade} 
                confidence={result.confidence} 
                />
                
                {/* Reset Button after result */}
                <div className="mt-8 text-center">
                    <button 
                        onClick={handleClearFile}
                        className="px-6 py-2 border-2 border-slate-300 text-slate-600 font-semibold rounded-lg hover:bg-slate-50 transition-colors"
                    >
                        Analyze Another Image
                    </button>
                </div>
            </div>
          )}

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-6 text-center text-xs">
        <p>© 2024 RetinaAI Project. For educational and research purposes only.</p>
        <p className="mt-1">Not intended for clinical diagnosis. Consult a doctor.</p>
      </footer>
    </div>
  );
}

export default App;