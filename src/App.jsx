import React, { useState } from "react";
import axios from "axios";
import trafficLight from "./assets/traffic-light.gif";

function App() {
  const [file, setFile] = useState(null);
  const [trafficData, setTrafficData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [videoOutput, setVideoOutput] = useState(null);

  // ✅ Add state for thresholds
  const [heavyThreshold, setHeavyThreshold] = useState(15);
  const [moderateThreshold, setModerateThreshold] = useState(10);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setTrafficData(null);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please upload a file first.");

    const formData = new FormData();
    formData.append("file", file);

    formData.append("heavy_threshold", heavyThreshold);
    formData.append("moderate_threshold", moderateThreshold);

    try {
      setLoading(true);
      const response = await axios.post(
        "http://localhost:5000/api/detect",
        formData,
        {
          responseType: "blob",
        }
      );

      const videoURL = URL.createObjectURL(
        new Blob([response.data], { type: "video/mp4" })
      );
      setVideoOutput(videoURL);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Detection failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex justify-center items-center">
      <div className="flex flex-row items-center justify-center w-full gap-8 p-4">
        {/* Left Traffic Light */}
        <div className="flex-shrink-0">
          <img src={trafficLight} alt="Traffic Light" className="w-32 h-auto" />
        </div>

        {/* Main Content */}
        <div className="flex flex-col items-center bg-white shadow-lg rounded-lg p-8 w-full max-w-xl">
          <h1 className="text-3xl font-bold mb-4 text-center">
            Traffic Congestion Detection
          </h1>

          <input
            type="file"
            accept="image/*,video/*"
            onChange={handleFileChange}
            className="mb-10 hover:bg-blue-200 bg-white shadow-lg border-1 rounded-md border-gray-300 p-2 "
          />

          {/* Threshold Inputs */}
          {/* Threshold Inputs */}
          <div className="grid grid-cols-2 gap-6 mb-4 w-full">
            {/* Moderate Traffic */}
            <div className="flex flex-col">
              <label
                htmlFor="moderateThreshold"
                className="text-gray-700 font-medium mb-2 text-center"
              >
                Moderate Traffic Vehicle Count Starts At
              </label>
              <input
                id="moderateThreshold"
                type="number"
                value={moderateThreshold}
                onChange={(e) => setModerateThreshold(Number(e.target.value))}
                className="border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-300 text-center"
                placeholder="e.g. 10"
              />
            </div>

            {/* Heavy Traffic */}
            <div className="flex flex-col">
              <label
                htmlFor="heavyThreshold"
                className="text-gray-700 font-medium mb-2 text-center"
              >
                Heavy Traffic Vehicle Count Starts At
              </label>
              <input
                id="heavyThreshold"
                type="number"
                value={heavyThreshold}
                onChange={(e) => setHeavyThreshold(Number(e.target.value))}
                className="border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-300 text-center"
                placeholder="e.g. 15"
              />
            </div>
          </div>

          <button
            onClick={handleUpload}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-500 font-semibold"
          >
            {loading ? "Processing..." : "Upload & Detect"}
          </button>

          {videoOutput && (
            <div className="mt-6 w-full text-center">
              <h2 className="text-xl font-semibold mb-2">
                Detection Result Video:
              </h2>
              <video
                key={videoOutput} // Force re-render
                src={videoOutput}
                width="700"
                height="500"
                controls
                autoPlay
                muted
              />
            </div>
          )}

          {trafficData && (
            <div className="mt-4 p-4 bg-gray-100 rounded shadow-inner w-full">
              <h3 className="text-lg font-bold mb-2">Traffic Info:</h3>
              <p>
                <strong>FPS:</strong> {trafficData.fps}
              </p>
              <p>
                <strong>Total Vehicles:</strong> {trafficData.total_cars}
              </p>
              <p>
                <strong>Left Street Cars:</strong>{" "}
                {trafficData.left_street_cars}
              </p>
              <p>
                <strong>Right Street Cars:</strong>{" "}
                {trafficData.right_street_cars}
              </p>
              <p>
                <strong>Traffic Condition:</strong> {trafficData.road_condition}
              </p>
            </div>
          )}
        </div>

        {/* Right Traffic Light */}
        <div className="flex-shrink-0">
          <img src={trafficLight} alt="Traffic Light" className="w-32 h-auto" />
        </div>

        <div></div>
      </div>
    </div>
  );
}

export default App;
