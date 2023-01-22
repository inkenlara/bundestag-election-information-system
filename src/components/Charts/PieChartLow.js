import React, { useState, useEffect } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

import { Pie, Bar } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChartLow = () => {
  const [data, setData] = useState([]);
  const getData = () => {
    fetch("http://localhost:8000/query9_low")
      .then(function (response) {
        console.log(response);
        return response.json();
      })
      .then(function (myJson) {
        console.log(myJson);
        setData(myJson);
      });
  };
  useEffect(() => {
    getData();
  }, []);
  var options = {
    maintainAspectRatio: false,
    scales: {},
    legend: {
      labels: {
        fontSize: 25,
      },
    },
    layout: {
      padding: 100,
    },
    plugins: {
      title: {
        display: true,
        text: "Geringste Bildung",
        font: {
          size: 18
      }
      },
    },
  };

  var vals = {
    labels: Object.keys(data),
    datasets: [
      {
        // afd, cdu, csu, linke, fdp, grune, spd
        label: "Durchschnittlicher Stimmenanteil in %",
        data: Object.values(data),
        backgroundColor: [
          "rgba(0, 153, 255, 0.2)",
          "rgba(0, 0, 0, 0.2)",
          "rgba(0, 0, 153, 0.2)",
          "rgba(255, 0, 153, 0.2)",
          "rgba(238, 255, 0, 0.2)",
          "rgba(30, 252, 10, 0.2)",
          "rgba(222, 78, 97, 0.2)",
        ],
        borderColor: [
          "rgba(0, 153, 255, 1)",
          "rgba(0, 0, 0, 1)",
          "rgba(0, 0, 153, 1)",
          "rgba(255, 0, 153, 1)",
          "rgba(238, 255, 0, 1)",
          "rgba(30, 252, 10, 1)",
          "rgba(222, 78, 97, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <Bar data={vals} height={600} options={options} />
    </div>
  );
};

export default PieChartLow;
