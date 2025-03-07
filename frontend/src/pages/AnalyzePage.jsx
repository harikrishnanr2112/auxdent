import { useState } from "react";
import axios from "axios";

const AnalyzePage = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload an image first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/analyze/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResults(response.data.detections);
    } catch (error) {
      console.error("Error analyzing image:", error);
      alert("An error occurred while analyzing the image.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-page">
      <h1>Analyze Dental X-ray</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {results && (
        <div className="results">
          <h2>Analysis Results</h2>
          {results.map((result, index) => (
            <div key={index} className="result-item">
              <h3>{result.class}</h3>
              <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
              <p>Bounding Box: {JSON.stringify(result.bbox)}</p>
              <p>Description: {result.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AnalyzePage;