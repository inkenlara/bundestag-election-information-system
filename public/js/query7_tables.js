

const kreise = ['Flensburg – Schleswig', 'Nordfriesland – Dithmarschen Nord', 'Steinburg – Dithmarschen Süd', 'Rendsburg-Eckernförde', 'Kiel'];
var val = 1;

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
    value = kreise.indexOf(this.value) + 1;
    console.log(value)
    fetch("http://localhost:8000/query7_wahlbeteiligung/" + value.toString()).then(function(response) {
        return response.json();
      }).then(function(data) {
        const newContent = document.createElement('p');        
        var tag_id = document.getElementById('wahlbet7');
        tag_id.innerHTML = data["data"];
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      });

    fetch("http://localhost:8000/query7_direktkandidaten/" + value.toString()).then(function(response) {
        return response.json();
      }).then(function(data) {
        const newContent = document.createElement('p');        
        var tag_id = document.getElementById('direktkand7');
        tag_id.innerHTML = data["data"];
        
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      });


    fetch("http://localhost:8000/query7_stimmen_entwicklung/" + value.toString()).then(function(response) {
        return response.json();
      }).then(function(data) {
        const newContent = document.createElement('p');        
        var tag_id = document.getElementById('p_entw7');
        tag_id.innerHTML = data["data"];
        
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      });

}

