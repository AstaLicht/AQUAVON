import { useEffect, useState } from "react";
import axios from "axios";
import LineChartDisplay from "./components/LineChartDisplay";

type SensorData = {
  time: string;
  temperature: number;
  ph: number;
  tds: number;
  turbidity: number;
};


type PredictionResponse = {
  temperature: number;
  ph: number;
  tds: number;
  turbidity: number;
  "Dissolved Oxygen (DO)": number;
  "Heavy Metal Concentration": string;
  "Bacterial Contamination": string;
};

export default function App() {
  const [data, setData] = useState<PredictionResponse | null>(null);
  const [chartData, setChartData] = useState<SensorData[]>([]);
  const [lastUpdated, setLastUpdated] = useState("");

  const fetchPredictions = async () => {
    try {
      const response = await axios.get("https://water-predictor-backend.onrender.com/predict");
      const result: PredictionResponse = response.data;

      setData(result);
      setLastUpdated(new Date().toLocaleTimeString());

      setChartData((prev) => [
        ...prev.slice(-19),
        {
          time: new Date().toLocaleTimeString(),
          temperature: result.temperature,
          ph: result.ph,
          tds: result.tds,
          turbidity: result.turbidity,
        },
      ]);
    } catch (err) {
      console.error("Error fetching prediction:", err);
    }
  };

  useEffect(() => {
    fetchPredictions(); // Initial fetch

    const interval = setInterval(fetchPredictions, 5000); // Every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-2">🌊 'AQUAVON'- Water Quality Dashboard</h1>
      <p className="text-gray-600 mb-4">Last updated at: {lastUpdated}</p>

      {data ? (
        <div className="bg-white p-6 rounded shadow w-full max-w-2xl">
          <p><strong>Temperature:</strong> {data.temperature} °C</p>
          <p><strong>pH:</strong> {data.ph}</p>
          <p><strong>TDS:</strong> {data.tds} ppm</p>
          <p><strong>Turbidity:</strong> {data.turbidity} NTU</p>
          <p><strong>Dissolved Oxygen:</strong> {data["Dissolved Oxygen (DO)"]}</p>
          <p><strong>Heavy Metals:</strong> {data["Heavy Metal Concentration"]}</p>
          <p><strong>Bacteria Status:</strong> {data["Bacterial Contamination"]}</p>
        </div>
      ) : (
        <p>Loading data...</p>
      )}

      <div className="w-full max-w-2xl mt-8">
        <LineChartDisplay data={chartData} />
      </div>
    </div>
  );
}
