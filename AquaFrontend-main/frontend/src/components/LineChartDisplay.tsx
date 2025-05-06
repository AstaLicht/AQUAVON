import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

type ChartProps = {
  data: any[];
  param: string;
  color: string;
};

const LineChartDisplay = ({ data, param, color }: ChartProps) => {
  const values = data.map((entry) => entry[param]);
  const adjustedColor = param === "do" ? "#38bdf8" : color;

  const chartData: ChartData<"line"> = {
    labels: data.map((entry) => entry.time),
    datasets: [
      {
        label: param.toUpperCase(),
        data: values,
        borderColor: adjustedColor,
        backgroundColor: adjustedColor + "66", // semi-transparent fill
        fill: true,
      },
    ],
  };

  const options: ChartOptions<"line"> = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: param === "do" ? true : false,
        min: param === "do" ? 0 : undefined,
        max: param === "do" ? 10 : undefined,
        ticks: {
          color: "#4B5563",
        },
      },
      x: {
        ticks: {
          color: "#ffffff", // white x-axis time labels
        },
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default LineChartDisplay;
