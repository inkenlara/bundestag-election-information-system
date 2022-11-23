google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Partei', 'Votes'],
          ['p1',     11],
          ['p2',      2],
          ['p3',  2],
          ['p4', 2],
          ['p5',    7]
        ]);

        var options = {
          //title: 'Sitzverteilung'
        };

        var chart = new google.visualization.PieChart(document.getElementById('sitzverteilung_chart'));

        chart.draw(data, options);
      }