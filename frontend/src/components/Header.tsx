export default function Header() {
  return (
    <header className="bg-blue-900 text-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        
        {/* Left Side: Logo & Title */}
        <div className="flex items-center gap-3">
          {/* Eye Icon */}
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            strokeWidth={1.5} 
            stroke="currentColor" 
            className="w-8 h-8 text-blue-300"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          
          <div>
            <h1 className="text-xl font-bold tracking-tight leading-tight">
              RetinaAI
            </h1>
            <p className="text-xs text-blue-200 font-medium">
              Diabetic Retinopathy Screener
            </p>
          </div>
        </div>

        {/* Right Side: Optional Info */}
        <div className="hidden md:block text-right">
          <p className="text-sm font-semibold opacity-90">Deep Learning Powered</p>
          <p className="text-xs text-blue-300">InceptionV3 Model</p>
        </div>

      </div>
    </header>
  );
}