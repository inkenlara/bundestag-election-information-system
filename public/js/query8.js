google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    //console.log(q8_data)
    var data = google.visualization.arrayToDataTable([
        ['Partei', 'Votes'],
        ['p1',     11],
        ['p2',      2],
        ['p3',  2],
        ['p4', 2],
        ['p5',    7]
    ]);

    var options = {
        'is3D':true,
        'width':600,
        'height':600
        //title: 'Sitzverteilung'
    };
    // var chart = new google.visualization.PieChart(document.getElementById('query8-reich'));
    // chart.draw(data, options);


    var data = google.visualization.arrayToDataTable([
        ['Partei', 'Votes'],
        ['p1',     11],
        ['p2',      2],
        ['p3',  2],
        ['p4', 2],
        ['p5',    7]
    ]);

    var options = {
        'is3D':true,
        'width':600,
        'height':600
        //title: 'Sitzverteilung'
    };
    // var chart = new google.visualization.PieChart(document.getElementById('query8-arm'));
    // chart.draw(data, options);

}