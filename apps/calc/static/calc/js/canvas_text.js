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
                borderColor: 'rgba(100, 100, 255, 1)',
                borderWidth: 2,
                showLine: true,
                lineTension: 0,
            }, {
                label: "Red Champ HP",
                data: [
                ],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 2,
                showLine: true,
                lineTension: 0,
            }
        ]
        },
        options: {
            legend: {
                labels: {
                    fontColor: "white"
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        beginAtZero:true
                    },
                }],
                xAxes: [{
                    ticks: {
                        min: 0,
                    },
                }]
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data.datasets[tooltipItem.datasetIndex].label || '';
            
                        if (label) {
                            label += ': ';
                        }
                        label += tooltipItem.yLabel.toFixed(0);
                        return label;
                    }
                }
            }

        }
    });
    function get_items(color) {
        var item_ids = [];
        var imgs = document.querySelectorAll("."+color+"-champ img.item");
        for (let i=0; i< imgs.length; i++) {
            if (imgs[i].currentSrc != "http://localhost:8000/static/calc/img/black_square.png") {
                item_ids.push(imgs[i].currentSrc.slice(44,48))
            }
        }
        return item_ids;
    }
    $("input.run-combat-submit").click(function(_e){
        //Get champs
        var blue_champ_name = "Ahri";
        var red_champ_name = "Ekko";
        var blue_items = [];
        var red_items = [];
        var blue_level = 1;
        var red_level = 1;
        blue_champ_name = $(".blue-champ img.champ-icon")[0].attributes.src.nodeValue.slice(30,-4);
        red_champ_name = $(".red-champ img.champ-icon")[0].attributes.src.nodeValue.slice(30,-4);
        blue_items = get_items("blue");
        red_items = get_items("red");
        blue_level = $(".blue-champ select option:selected").val();
        red_level = $(".red-champ select option:selected").val();
        $.ajax("/run_combat", {
            data: {
                blue_champ: blue_champ_name,
                red_champ: red_champ_name,
                blue_items: blue_items,
                red_items: red_items,
                blue_level: blue_level,
                red_level: red_level,
            },
            success: (function(data){
                //clear old data
                myChart.data.datasets[0].data = [];
                myChart.data.datasets[1].data = [];
                //Add new data
                myChart.data.datasets[0].label = blue_champ_name+" HP";
                myChart.data.datasets[1].label = red_champ_name+" HP";
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
            }),
            error: function(data) {
                console.log(data);
            }
        });
    });
});