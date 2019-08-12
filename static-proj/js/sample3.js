
var endpoint = '/sample'

        $.ajax({
                method: "GET",
                url: endpoint,
        success: function(data){
            var ctx = document.getElementById("myChart2").getContext('2d');
            var myChart = new Chart(ctx, {
            type: 'doughnut',
                data: {
labels:["Delhi", "Maharashtra"],
                       datasets: [{
                                label: 'Locations',
                                 data: data.data,
            backgroundColor: [
                'rgba(120, 99, 132, 0.6)',
              'rgba(54, 162, 235, 0.8)',

                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',

                                ],
                            borderWidth: 1
                                            }]
                                                },

                                                                });
                                                            },
                          error: function(error_data){

                            console.log(error_data)
                                }
                                                })

setTimeout( 1000);