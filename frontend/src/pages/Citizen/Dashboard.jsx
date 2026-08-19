import { useState } from "react";
import axios from "axios";

function Dashboard() {
  const [applicationType, setApplicationType] = useState("Scholarship");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const uploadFile = async () => {
    if (!file) {
      setError("Please choose a PDF file.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
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
      console.error("Upload error:", error);

      if (error.response) {
        setError(
          `Upload failed: ${
            error.response.data?.detail || "Server error"
          }`
        );
      } else {
        setError(
          "Unable to connect to the backend. Make sure FastAPI is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    if (status === "Valid") {
      return "bg-green-100 text-green-700 border-green-300";
    }

    if (status === "Invalid") {
      return "bg-red-100 text-red-700 border-red-300";
    }

    return "bg-yellow-100 text-yellow-700 border-yellow-300";
  };

  return (
    <div className="min-h-screen bg-blue-50 p-6 md:p-10">

      {/* HEADER */}

      <div className="max-w-5xl mx-auto mb-8">
        <h1 className="text-4xl md:text-5xl font-bold text-center text-blue-600">
          Citizen Dashboard
        </h1>

        <p className="text-center text-gray-600 mt-3">
          Upload your document and verify it using AI-powered semantic
          validation.
        </p>
      </div>

      {/* MAIN CARD */}

      <div className="max-w-5xl mx-auto bg-white rounded-3xl shadow-lg p-6 md:p-10">

        <h2 className="text-2xl font-bold text-gray-800 mb-8">
          Semantic Validation
        </h2>

        {/* APPLICATION TYPE */}

        <div className="mb-6">

          <label className="block font-semibold text-gray-700 mb-2">
            Select Application
          </label>

          <select
            value={applicationType}
            onChange={(e) => setApplicationType(e.target.value)}
            className="w-full border border-gray-300 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            <option>Scholarship</option>
            <option>Income Certificate</option>
            <option>Educational Application</option>
            <option>Government Application</option>
          </select>

        </div>

        {/* FILE UPLOAD */}

        <div className="mb-6">

          <label className="block font-semibold text-gray-700 mb-2">
            Upload PDF
          </label>

          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setError("");
              setResult(null);
            }}
            className="w-full border border-gray-300 rounded-xl p-3 bg-gray-50"
          />

          {file && (
            <p className="text-sm text-gray-500 mt-2">
              Selected file: <strong>{file.name}</strong>
            </p>
          )}

        </div>

        {/* ERROR */}

        {error && (
          <div className="mb-6 bg-red-50 border border-red-300 text-red-700 rounded-xl p-4">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* UPLOAD BUTTON */}

        <button
          onClick={uploadFile}
          disabled={loading}
          className={`w-full rounded-xl py-4 text-white font-semibold text-lg transition ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600 hover:shadow-lg"
          }`}
        >
          {loading ? "Validating Document..." : "Upload & Validate"}
        </button>

        {/* RESULT */}

        {result && (
          <div className="mt-10">

            {/* RESULT HEADER */}

            <div className="border-b pb-5 mb-6">

              <h3 className="text-2xl font-bold text-gray-800">
                Validation Result
              </h3>

              <p className="text-gray-500 mt-1">
                AI-powered analysis of your uploaded document
              </p>

            </div>

            {/* BASIC INFORMATION */}

            <div className="grid md:grid-cols-2 gap-4 mb-6">

              <div className="bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-gray-500">
                  File Name
                </p>

                <p className="font-semibold text-gray-800 break-all">
                  {result.filename}
                </p>
              </div>

              <div className="bg-gray-50 rounded-xl p-4">
                <p className="text-sm text-gray-500">
                  Detected Intent
                </p>

                <p className="font-semibold text-gray-800">
                  {result.intent || "Unknown"}
                </p>
              </div>

            </div>

            {/* VALIDATION STATUS */}

            {result.validation && (
              <div className="mb-6">

                <div className="bg-gray-50 rounded-2xl p-6">

                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">

                    <div>

                      <p className="text-sm text-gray-500 mb-1">
                        Validation Status
                      </p>

                      <span
                        className={`inline-block px-4 py-2 rounded-full border font-bold ${getStatusColor(
                          result.validation.status
                        )}`}
                      >
                        {result.validation.status}
                      </span>

                    </div>

                    <div>

                      <p className="text-sm text-gray-500 mb-1">
                        Validation Score
                      </p>

                      <p className="text-3xl font-bold text-blue-600">
                        {result.validation.score ?? 0}
                        <span className="text-lg text-gray-400">
                          /100
                        </span>
                      </p>

                    </div>

                  </div>

                </div>

              </div>
            )}

            {/* ERRORS */}

            {result.validation?.errors?.length > 0 && (
              <div className="mb-6">

                <h4 className="text-xl font-bold text-red-600 mb-3">
                  Validation Errors
                </h4>

                <div className="space-y-3">

                  {result.validation.errors.map((errorItem, index) => (
                    <div
                      key={index}
                      className="bg-red-50 border border-red-200 rounded-xl p-4"
                    >

                      <p className="font-bold text-red-700">
                        {errorItem.type}
                      </p>

                      <p className="text-red-600 mt-1">
                        {errorItem.message}
                      </p>

                    </div>
                  ))}

                </div>

              </div>
            )}

            {/* WARNINGS */}

            {result.validation?.warnings?.length > 0 && (
              <div className="mb-6">

                <h4 className="text-xl font-bold text-yellow-600 mb-3">
                  Warnings
                </h4>

                <div className="space-y-3">

                  {result.validation.warnings.map((warning, index) => (
                    <div
                      key={index}
                      className="bg-yellow-50 border border-yellow-200 rounded-xl p-4"
                    >

                      <p className="font-bold text-yellow-700">
                        {warning.type}
                      </p>

                      <p className="text-yellow-700 mt-1">
                        {warning.message}
                      </p>

                    </div>
                  ))}

                </div>

              </div>
            )}

            {/* EXTRACTED ENTITIES */}

            {result.entities && (
              <div className="mb-6">

                <h4 className="text-xl font-bold text-gray-800 mb-4">
                  Extracted Information
                </h4>

                <div className="grid md:grid-cols-2 gap-4">

                  {/* DATES */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Dates
                    </p>

                    {result.entities.dates?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.dates.map((date, index) => (
                          <li key={index}>{date}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                  {/* MONEY */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Money
                    </p>

                    {result.entities.money?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.money.map((money, index) => (
                          <li key={index}>{money}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                  {/* UNIVERSITIES */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Universities / Institutions
                    </p>

                    {result.entities.universities?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.universities.map(
                          (university, index) => (
                            <li key={index}>{university}</li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                  {/* COURSES */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Courses
                    </p>

                    {result.entities.courses?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.courses.map(
                          (course, index) => (
                            <li key={index}>{course}</li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                  {/* NAMES */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Names
                    </p>

                    {result.entities.names?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.names.map((name, index) => (
                          <li key={index}>{name}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                  {/* IDENTIFICATION NUMBERS */}

                  <div className="bg-blue-50 rounded-xl p-4">

                    <p className="font-semibold text-gray-700">
                      Identification Numbers
                    </p>

                    {result.entities.identification_numbers?.length > 0 ? (
                      <ul className="mt-2 text-gray-600 list-disc list-inside">
                        {result.entities.identification_numbers.map(
                          (id, index) => (
                            <li key={index}>{id}</li>
                          )
                        )}
                      </ul>
                    ) : (
                      <p className="text-gray-400 mt-2">
                        None detected
                      </p>
                    )}

                  </div>

                </div>

              </div>
            )}

            {/* ACADEMIC RECORDS */}

            {result.entities?.academic_records?.length > 0 && (
              <div className="mb-6">

                <h4 className="text-xl font-bold text-gray-800 mb-4">
                  Academic Records
                </h4>

                <div className="overflow-x-auto">

                  <table className="w-full border-collapse">

                    <thead>
                      <tr className="bg-blue-100">
                        <th className="border p-3 text-left">
                          Year
                        </th>

                        <th className="border p-3 text-left">
                          Maximum Marks
                        </th>

                        <th className="border p-3 text-left">
                          Obtained Marks
                        </th>

                        <th className="border p-3 text-left">
                          Percentage
                        </th>
                      </tr>
                    </thead>

                    <tbody>

                      {result.entities.academic_records.map(
                        (record, index) => (
                          <tr key={index}>

                            <td className="border p-3">
                              {record.year}
                            </td>

                            <td className="border p-3">
                              {record.maximum_marks}
                            </td>

                            <td className="border p-3">
                              {record.obtained_marks}
                            </td>

                            <td className="border p-3">
                              {record.percentage}%
                            </td>

                          </tr>
                        )
                      )}

                    </tbody>

                  </table>

                </div>

              </div>
            )}

            {/* INCOME */}

            {result.entities?.income &&
              (result.entities.income.monthly !== null ||
                result.entities.income.annual !== null) && (
                <div className="mb-6">

                  <h4 className="text-xl font-bold text-gray-800 mb-4">
                    Income Information
                  </h4>

                  <div className="grid md:grid-cols-2 gap-4">

                    <div className="bg-green-50 rounded-xl p-4">
                      <p className="text-sm text-gray-500">
                        Monthly Income
                      </p>

                      <p className="text-xl font-bold text-green-700">
                        ₹
                        {result.entities.income.monthly?.toLocaleString(
                          "en-IN"
                        ) || "Not detected"}
                      </p>
                    </div>

                    <div className="bg-green-50 rounded-xl p-4">
                      <p className="text-sm text-gray-500">
                        Annual Income
                      </p>

                      <p className="text-xl font-bold text-green-700">
                        ₹
                        {result.entities.income.annual?.toLocaleString(
                          "en-IN"
                        ) || "Not detected"}
                      </p>
                    </div>

                  </div>

                </div>
              )}

            {/* EXTRACTED TEXT */}

            <div className="mb-4">

              <h4 className="text-xl font-bold text-gray-800 mb-3">
                Extracted Text
              </h4>

              <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 max-h-80 overflow-auto">

                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-sans">
                  {result.extracted_text || "No text extracted."}
                </pre>

              </div>

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default Dashboard;