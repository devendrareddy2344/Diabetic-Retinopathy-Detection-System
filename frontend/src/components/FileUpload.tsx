import { ChangeEvent } from "react";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  isLoading: boolean;
}

export default function FileUpload({ onFileSelect, isLoading }: FileUploadProps) {
  
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    // Safety check to ensure a file was actually selected
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="w-full">
      <label 
        htmlFor="file-upload"
        // The backticks (`) here are critical for the ${} logic to work
        className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-xl cursor-pointer transition-colors ${
          isLoading 
            ? "bg-gray-100 border-gray-300 opacity-50 cursor-not-allowed" 
            : "bg-white border-blue-300 hover:bg-blue-50 hover:border-blue-500"
        }`}
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4">
          <svg className="w-12 h-12 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="mb-2 text-lg text-gray-700 font-medium">
            <span className="font-bold text-blue-600">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-gray-500">
            Fundus Image (PNG, JPG, JPEG)
          </p>
        </div>
        
        <input 
          id="file-upload" 
          type="file" 
          className="hidden" 
          accept="image/*"
          onChange={handleInputChange}
          disabled={isLoading}
        />
      </label>
    </div>
  );
}