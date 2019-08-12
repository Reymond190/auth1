
var endpoint = '/sample'

        $.ajax({
                method: "GET",
                url: endpoint,
        success: function(data){

            var ctx = document.getElementById("myChart").getContext('2d');
            var myChart = new Chart(ctx, {
            type: 'pie',
                data: {
                        labels: data.labels,
                       datasets: [{
                                label: 'Engine',
                                 data: data.data,
            backgroundColor: [
                'rgba(255, 99, 71, 0.6)',
            'rgb(255, 165, 00.8)'

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