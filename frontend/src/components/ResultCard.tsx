interface ResultProps {
  diagnosis: string;
  severity: number;
  confidence: number;
}

export default function ResultCard({ diagnosis, severity, confidence }: ResultProps) {
  
  // Dynamic styling based on severity grade
  const getStatusColor = () => {
    if (severity === 0) return "bg-green-50 border-green-200 text-green-800"; // No DR
    if (severity === 1) return "bg-blue-50 border-blue-200 text-blue-800";    // Mild
    if (severity === 2) return "bg-yellow-50 border-yellow-200 text-yellow-800"; // Moderate
    return "bg-red-50 border-red-200 text-red-800"; // Severe/Proliferative
  };

  const getRecommendation = () => {
    if (severity === 0) return "Routine annual screening recommended.";
    if (severity <= 2) return "Schedule appointment with ophthalmologist within 4-8 weeks.";
    return "Urgent referral to retinal specialist required.";
  };

  return (
    <div className={`mt-8 p-6 rounded-xl border-2 ${getStatusColor()} shadow-sm transition-all animate-fade-in`}>
      <h2 className="text-lg font-bold uppercase tracking-wide mb-4 border-b border-black/10 pb-2">Analysis Report</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <p className="text-xs uppercase opacity-70 font-semibold">Diagnosis</p>
          <p className="text-2xl font-extrabold mt-1">{diagnosis}</p>
        </div>
        
        <div>
          <p className="text-xs uppercase opacity-70 font-semibold">AI Confidence</p>
          <p className="text-2xl font-extrabold mt-1">{confidence}%</p>
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-black/10">
        <p className="text-sm font-medium">
          <span className="font-bold">Next Step:</span> {getRecommendation()}
        </p>
      </div>
    </div>
  );
}