$(function() {
    var ctx = $(".canvas-graph");
    var myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Blue Champ HP',
                data: [
                ],
                backgroundColor: 'rgba(0, 0, 160, 0.2)',
                borderColor: 'rgba(20, 20, 255, 0.8)',
                borderWidth: 1,
                showLine: true,
                lineTension: 0,

            }, {
                label: "Red Champ HP",
                data: [
                ],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
                showLine: true,
                lineTension: 0,

            }
        ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                    ticks: {
                        min: 0,
                    }
                }]
            }
        }
    });
    $("input.run-combat-submit").click(function(e){
        $.ajax("/run_combat", {success: (function(data){
            //clear old data
            myChart.data.datasets[0].data = [];
            myChart.data.datasets[1].data = [];

            //Add new data
            let xhr_blue_data = data["blue-champ"];
            let chart_blue_data = myChart.data.datasets[0].data;
            for (let i=0; i< xhr_blue_data.length; i++) {
                chart_blue_data.push(xhr_blue_data[i]);
            }
            let chart_red_data = myChart.data.datasets[1].data;
            let xhr_red_data = data["red-champ"];
            for (let i=0; i< xhr_red_data.length; i++) {
                chart_red_data.push(xhr_red_data[i]);
            }
            myChart.update()
        })});
    });
});