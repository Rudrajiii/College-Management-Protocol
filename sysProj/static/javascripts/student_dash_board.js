fetch("/access_data")
  .then((response) => response.json())
  .then((data) => {

    const departments = {};

    for (const student of data) {
      const department = student.department;
      departments[department] = (departments[department] || 0) + 1;
    }

    const dataForChart = {
      labels: Object.keys(departments),
      datasets: [
        {
          data: Object.values(departments),
          backgroundColor: [
            "#ffbb99", // Orange
            "#99ff99", // Green
            "#ff99ff", // Pink
            "#c2c2f0", // Light blue
            "#f0c2c2", // Light red
            "#c2f0f0", // Light blue-green
            "#cccccc", // Light gray
            "#ffb3b3", // Light pink
            "#99ccff", // Light sky blue
            "#b3ffb3", // Light green
            "#ffcccc", // Light coral
            "#99e6e6", // Light cyan
            "#ffd966", // Light yellow
            "#d9b3ff", // Light purple
          ],
        },
      ],
    };

    const config = {
      type: "doughnut",
      data: dataForChart,
      options: {
        responsive: false, 
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
        plugins: {
          legend: {
            display: true, 
            position: "top", 
          },
        },
      },
    };

    const ctx = document.getElementById("myChart").getContext("2d");
    const myChart = new Chart(ctx, config);
  })
  .catch((error) => console.error("Error fetching JSON:", error));
