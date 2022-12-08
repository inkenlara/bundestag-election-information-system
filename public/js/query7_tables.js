google.charts.load('current', {'packages':['corechart']});
        const kreise = ['Flensburg – Schleswig', 'Nordfriesland – Dithmarschen Nord', 'Steinburg – Dithmarschen Süd', 'Rendsburg-Eckernförde', 'Kiel'];
        var val = 1;
        // radio group generation        
        //this.value = ;
        const group = document.querySelector("#group");
        group.innerHTML = kreise.map((kreis) => `<div>
                <input type="radio" name="kreis" value="${kreis}" id="${kreis}">
                 <label for="${kreis}">${kreis}</label>
            </div>`).join(' ');
        
        // event listener
        const radioButtons = document.querySelectorAll('input[name="kreis"]');
        for(const radioButton of radioButtons){
            radioButton.addEventListener('change', showSelected);
        }        
        
        function showSelected(e) {
            value = this.value;
            console.log(kreise.indexOf(value) + 1);
            google.charts.setOnLoadCallback(draw_c);
        }
        // in kreise.indexOf(value) + 1 is stored which wahlkreis is chosen, that can be used to filter out the SQL results
        function draw_c() {
            var data1 = google.visualization.arrayToDataTable([   // just as an example
                ['Partei', 'Votes'],
                ['p1',     kreise.indexOf(value) + 1],
                ['p2',      2],
                ['p3',  2],
                ['p4', 2],
                ['p5',    7]
            ]);
            var options = {
                'is3D':true
            };
            var chart = new google.visualization.PieChart(document.getElementById('q7'));
            chart.draw(data1, options);
        }