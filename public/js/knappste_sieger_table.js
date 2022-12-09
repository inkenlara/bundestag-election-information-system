/* 
google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Vorname');
        data.addColumn('string', 'Nachname');
        data.addColumn('string', 'Partei');
        data.addRows([
          ['v1', 'n1', 'p1'],
          ['v2', 'n2', 'p2'],
          ['v3', 'n3', 'p3'],
          ['v4', 'n4', 'p4']
        ]);
        var table = new google.visualization.Table(document.getElementById('knappste_sieger_table'));
        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});

        data = new google.visualization.DataTable();
        data.addColumn('string', 'Partei');
        data.addColumn('string', 'WahlKreis')
        data.addRows([
          ['p1', 'w1'],
          ['p2', 'w2'],
          ['p3', 'w3'],
          ['p4', 'w4']
        ]);
        var table = new google.visualization.Table(document.getElementById('knappste_verlierer'));
        table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});

      } */