 var endpoint = '/sample1';

   $.ajax({
                method: "GET",
                url: endpoint,
        success: function(data){
	  var ctx = document.getElementById("myChart1").getContext('2d');

var chartOptions = {
  scales: {
    xAxes: [{

      gridLines: {
        display: false
      },
 scaleLabel: {
        display: true,
        labelString: "Speed of Vechicles"
      }
    }],
    yAxes: [{
      gridLines: {
        zeroLineColor: "black",
        zeroLineWidth: 2
      },
ticks: {
        min: 0,
        max: 500,
        stepSize: 100
      },
      scaleLabel: {
        display: true,
        labelString: "Number of Vechicles"
      }
    }]
  },
  elements: {
    rectangle: {
      borderSkipped: 'left'
    }
  }
};
var densityData = {
  label: 'Speed',
  data: ["222","0","1","0","1","20","3"],
  backgroundColor: [
    'rgba(0, 99, 132, 0.6)',
    'rgba(30, 99, 132, 0.6)',
    'rgba(60, 99, 132, 0.6)',
    'rgba(90, 99, 132, 0.6)',
    'rgba(120, 99, 132, 0.6)',
    'rgba(150, 99, 132, 0.6)',
    'rgba(180, 99, 132, 0.6)',
    'rgba(210, 99, 132, 0.6)',
    'rgba(240, 99, 132, 0.6)'
  ],
  borderColor: [
    'rgba(0, 99, 132, 1)',
    'rgba(30, 99, 132, 1)',
    'rgba(60, 99, 132, 1)',
    'rgba(90, 99, 132, 1)',
    'rgba(120, 99, 132, 1)',
    'rgba(150, 99, 132, 1)',
    'rgba(180, 99, 132, 1)',
    'rgba(210, 99, 132, 1)',
    'rgba(240, 99, 132, 1)'
  ],
  borderWidth: 2,
  hoverBorderWidth: 0
};

            var myChart = new  Chart(ctx, {

            type: 'line',

                data: {
  labels: ["0", "20", "40", "60", "80", "100", "120"],

                 datasets: [densityData]},
 options: chartOptions

                                                                });
                                                            },
                          error: function(error_data){

                            console.log(error_data)
                                }
                                                });
                                    