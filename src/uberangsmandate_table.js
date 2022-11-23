google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Wahlkreis');
        data.addColumn('string', 'Partei');
        data.addColumn('string', 'Uberhangsmandate')
        data.addRows([
          ['w1', 'p1', 'p2'],
          ['w2', 'p3', 'p2'],
          ['w3', 'p4', 'p5'],
          ['w4', 'p2', 'p7']
        ]);

        var table = new google.visualization.Table(document.getElementById('uberangsmandate_table'));

        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});
      }