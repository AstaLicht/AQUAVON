import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

// 1. Define the type for sensor data
type SensorData = {
  time: string;
  temperature: number;
  ph: number;
  tds: number;
  turbidity: number;
};

// 2. Define props for the component
type Props = {
  data: SensorData[];
};

// 3. Add the type to the function definition here 👇
const LineChartDisplay = ({ data }: Props) => {
  const chartData = {
    labels: data.map((point) => point.time),
    datasets: [
      {
        label: "Temperature (°C)",
        data: data.map((point) => point.temperature),
        borderColor: "rgba(255, 99, 132, 1)",
        fill: false,
      },
      {
        label: "pH",
        data: data.map((point) => point.ph),
        borderColor: "rgba(54, 162, 235, 1)",
        fill: false,
      },
      {
        label: "TDS (ppm)",
        data: data.map((point) => point.tds),
        borderColor: "rgba(255, 206, 86, 1)",
        fill: false,
      },
      {
        label: "Turbidity (NTU)",
        data: data.map((point) => point.turbidity),
        borderColor: "rgba(75, 192, 192, 1)",
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" as const },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  return <Line data={chartData} options={options} />;
};

// 4. Export it at the bottom
export default LineChartDisplay;
