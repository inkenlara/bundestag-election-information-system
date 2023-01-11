import React, { Component } from "react";

class Wahlkreiserst extends Component {
  state = {
    value: 1,
  };
  render() {
    return (
      <React.Fragment>
        <h2 id="Wahlkreisubersicht_erst">Wahlkreisübersicht (Einzelstimmen)</h2>
        <select
          defaultValue={1}
          onChange={this.handleValue}
          id="wahlkreis_choice"
        >
          <option value="1">Flensburg – Schleswig</option>
          <option value="2">Nordfriesland – Dithmarschen Nord</option>
          <option value="3">Steinburg – Dithmarschen Süd</option>
          <option value="4">Rendsburg-Eckernförde</option>
          <option value="5">Kiel</option>
        </select>

        <h3>Wahlbeteiligung</h3>
        <div id="Wahlbeteiligung">
          <p id="wahlbet"></p>
          {this.renderTable1()}
        </div>
        <h3>Direktkandidaten</h3>
        <div id="Direktkandidaten_info">
          <p id="direktkand"></p>
          {this.renderTable2()}
        </div>
        <h3>Pro Partei, entwicklung</h3>
        <div id="partei_entw">
          <table id="p_entw"></table>
          {this.renderTable3()}
        </div>
      </React.Fragment>
    );
  }

  handleValue = () => {
    var menu = document.getElementById("wahlkreis_choice");
    this.setState({ value: menu.value });
    // console.log(this.state.value);
  };

  handlereq1() {
    fetch(
      "http://localhost:8000/query7_wahlbeteiligung/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("wahlbet");
        tag_id.innerHTML = data["data"];
        // console.log(this.state.value.toString());
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable1() {
    return this.handlereq1();
  }

  handlereq2() {
    fetch(
      "http://localhost:8000/query7_direktkandidaten/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("direktkand");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable2() {
    return this.handlereq2();
  }

  handlereq3() {
    fetch(
      "http://localhost:8000/query7_stimmen_entwicklung/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("p_entw");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable3() {
    this.handlereq3();
  }
}

export default Wahlkreiserst;
