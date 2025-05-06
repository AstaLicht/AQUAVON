import { useEffect, useState } from "react";
import axios from "axios";
import LineChartDisplay from "./components/LineChartDisplay";
import aquavonLogo from "./assets/Aquavon logo.png"; // Make sure the image is placed in /src/assets/
import "./App.css"; // For background animation styles

type ChartEntry = {
  time: string;
  temperature: number;
  ph: number;
  tds: number;
  turbidity: number;
  do: number;
  metal: number;
};

export default function App() {
  const [data, setData] = useState<any>(null);
  const [chartData, setChartData] = useState<ChartEntry[]>([]);
  const [lastUpdated, setLastUpdated] = useState("");

  const metalLevelToNumber = (metal: string): number => {
    switch (metal.toLowerCase()) {
      case "low":
        return 0;
      case "medium":
        return 1;
      case "high":
        return 2;
      default:
        return -1;
    }
  };

  const fetchPredictions = async () => {
    try {
      const response = await axios.get(
        "https://water-predictor-backend.onrender.com/predict"
      );
      const result = response.data;

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
          do: parseFloat(result["Dissolved Oxygen (DO)"]),
          metal: metalLevelToNumber(result["Heavy Metal Concentration"]),
        },
      ]);
    } catch (err) {
      console.error("Error fetching prediction:", err);
    }
  };

  useEffect(() => {
    fetchPredictions();
    const interval = setInterval(fetchPredictions, 2000);
    return () => clearInterval(interval);
  }, []);

  const parameters = [
    { key: "temperature", label: "Temperature (°C)", color: "#f87171" },
    { key: "ph", label: "pH", color: "#60a5fa" },
    { key: "tds", label: "TDS (ppm)", color: "#34d399" },
    { key: "turbidity", label: "Turbidity (NTU)", color: "#fbbf24" },
    { key: "do", label: "Dissolved Oxygen (mg/L)", color: "#a78bfa" },
    { key: "metal", label: "Heavy Metals (Low=0, High=2)", color: "#f472b6" },
  ];

  return (
    <div className="min-h-screen bg-cover bg-center bg-fixed custom-water-bg text-white p-4 flex flex-col items-center">
      {/* Header with logo */}
      <div className="flex flex-col items-center mb-4">
        <img src={aquavonLogo} alt="Aquavon Logo" className="w-32 mb-2" />
        <h1 className="text-3xl font-bold text-white">
          Intelligence in every drop
        </h1>
        <p className="text-white mt-1">Smart Water Quality Dashboard</p>
        <p className="text-sm text-gray-200 mt-1">
          Last updated at: {lastUpdated}
        </p>
      </div>

      {/* Current Values */}
      {data ? (
        <div className="bg-white bg-opacity-90 text-black p-6 rounded shadow w-full max-w-2xl mb-6">
          <p>
            <strong>Temperature:</strong> {data.temperature} °C
          </p>
          <p>
            <strong>pH:</strong> {data.ph}
          </p>
          <p>
            <strong>TDS:</strong> {data.tds} ppm
          </p>
          <p>
            <strong>Turbidity:</strong> {data.turbidity} NTU
          </p>
          <p>
            <strong>Dissolved Oxygen:</strong> {data["Dissolved Oxygen (DO)"]}
          </p>
          <p>
            <strong>Heavy Metals:</strong> {data["Heavy Metal Concentration"]}
          </p>
          <p>
            <strong>Bacteria Status:</strong> {data["Bacterial Contamination"]}
          </p>
        </div>
      ) : (
        <p>Loading data...</p>
      )}

      {/* Charts */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-6xl">
        {parameters.map((param) => (
          <div
            key={param.key}
            className="bg-white bg-opacity-90 rounded shadow p-4 h-72 w-full flex flex-col"
          >
            <h2 className="text-center text-lg font-semibold mb-2 text-black">
              {param.label}
            </h2>
            <LineChartDisplay
              data={chartData}
              param={param.key}
              color={param.color}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
