import { useState } from "react";
import axios from "axios";

function Dashboard() {
  const [applicationType, setApplicationType] = useState("Scholarship");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please choose a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-blue-50 p-10">

      <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">
        Citizen Dashboard
      </h1>

      <div className="max-w-2xl mx-auto bg-white rounded-3xl shadow-lg p-8">

        <h2 className="text-2xl font-semibold mb-6">
          Semantic Validation
        </h2>

        <label className="font-medium">
          Select Application
        </label>

        <select
          value={applicationType}
          onChange={(e) => setApplicationType(e.target.value)}
          className="w-full border rounded-xl p-3 mt-2 mb-6"
        >
          <option>Scholarship</option>
          <option>Income Certificate</option>
        </select>

        <label className="font-medium">
          Upload PDF
        </label>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="w-full mt-2 mb-6"
        />

        <button
          onClick={uploadFile}
          className="w-full bg-blue-500 text-white rounded-xl py-3 hover:bg-blue-600"
        >
          {loading ? "Uploading..." : "Upload & Validate"}
        </button>

        {result && (
          <div className="mt-8 bg-blue-100 rounded-xl p-5">

            <h3 className="text-xl font-bold mb-4">
              Validation Result
            </h3>

            <p>
              <strong>File:</strong> {result.filename}
            </p>

            <p>
              <strong>Intent:</strong> {result.intent}
            </p>

            <p className="mt-3">
              <strong>Extracted Text:</strong>
            </p>

            <div className="bg-white rounded-lg p-3 mt-2 max-h-64 overflow-auto">
              {result.text}
            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default Dashboard;