var value = 10;
google.charts.load('current', {'packages':['table']});
// google.charts.setOnLoadCallback(drawTable);

// var menu2 = document.getElementById("wahlkreis_choice2");
// menu2.addEventListener("change", set_value);

/* function set_value(event) {
    value = menu2.value; */
    google.charts.setOnLoadCallback(drawTable);
// }

///////////////

// The global variable value contains the Wahlkreis id, which can be used to filter the data
function drawTable() {
    let data = new google.visualization.DataTable();
    data.addColumn('number', 'Something...');
    data.addRows([
        [ parseInt(value)] // in value is Wahlkreis ID
    ]);
    var table = new google.visualization.Table(document.getElementById('q7'));
    table.draw(data, {showRowNumber: false, width: '100%', height: '100%'});
    
  }


