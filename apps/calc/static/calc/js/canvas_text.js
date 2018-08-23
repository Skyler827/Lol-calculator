$(function() {
    var ctx = $(".canvas-graph");
    var myChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Blue Champ HP',
                data: [
                    {x:0, y:100},
                    {x:1, y:85},
                    {x:2, y:70},
                    {x:3, y:100},
                    {x:4, y:50},
                    {x:5, y:20}
                ],
                backgroundColor: 'rgba(0, 0, 160, 0.2)',
                borderColor: 'rgba(20, 20, 255, 0.8)',
                borderWidth: 1,
                showLine: true,
            }, {
                label: "Red Champ HP",
                data: [
                    {x:0, y:150},
                    {x:1, y:20},
                    {x:2, y:10},
                    {x:3, y:30},
                    {x:4, y:5},
                    {x:5, y:0}
                ],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 1,
                showLine: true,

            }
        ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
});