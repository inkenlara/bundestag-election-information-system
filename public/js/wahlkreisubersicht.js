// var value = 10;
// google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable);

var menu = document.getElementById("wahlkreis_choice");
menu.addEventListener("change", set_value);


function set_value(event) {
    value = menu.value;
    //console.log(menu.value)

    var xmlHttp = new XMLHttpRequest();

    fetch("http://localhost:8000/query3_wahlbeteiligung/" + value.toString()).then(function(response) {
        return response.json();
      }).then(function(data) {
        const newContent = document.createElement('p');        
        var tag_id = document.getElementById('wahlbet');
        tag_id.innerHTML = data["data"];
        
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
    
      fetch("http://localhost:8000/query3_direktkandidaten/" + value.toString()).then(function(response) {
        return response.json();
      }).then(function(data) {
        const newContent = document.createElement('p');        
        var tag_id = document.getElementById('direktkand');
        tag_id.innerHTML = data["data"];
        
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      });

}






/* 
// The global variable value contains the Wahlkreis id, which can be used to filter the data
function drawTable() {
    let data = new google.visualization.DataTable();
    data.addColumn('number', 'WahlBeteiligung');
    data.addRows([
        [ parseInt(value)] // in value is Wahlkreis ID
    ]);
    var table = new google.visualization.Table(document.getElementById('Wahlbeteiligung'));
    table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});


    data = new google.visualization.DataTable();
    data.addColumn('string', 'DirektKandidat VorName');
    data.addColumn('string', 'DirektKandidat NachName');
    data.addRows([
        ['w1', 'p1'],
        ['w2', 'p3'],
        ['w3', 'p4'],
        ['w4', 'p2']
    ]);
    var table = new google.visualization.Table(document.getElementById('Direktkandidaten_table'));
    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});


    data = new google.visualization.DataTable();
    data.addColumn('string', 'Partei');
    data.addColumn('number', 'Anzahl Stimmen');
    data.addColumn('number', 'Prozent Stimmen')
    data.addRows([
        ['w1', 10, parseInt(value)],
        ['w2', 12, 2],
        ['w3', 3, 3],
        ['w4', 4, 4]
    ]);
    var table = new google.visualization.Table(document.getElementById('pro_partei'));
    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});

    // TODO figure out how to structure
    data = new google.visualization.DataTable();
    data.addColumn('string', 'TODO');
    data.addColumn('string', 'TODO');
    data.addColumn('number', 'TODO')
    data.addRows([
        ['w1', 'p1', parseInt(value)],
        ['w2', 'p3', 2],
        ['w3', 'p4', 3],
        ['w4', 'p2', 4]
    ]);
    var table = new google.visualization.Table(document.getElementById('entwicklung'));
    table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});


  }
*/

