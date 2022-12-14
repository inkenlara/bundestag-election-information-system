import React, { Component } from "react";

class Knappstesieger extends Component {
  state = {};
  render() {
    return (
      <React.Fragment>
        <h2 id="knappste">Knappste Sieger</h2>
        <p>
          die gewählten Erstkandidaten, welche mit dem geringsten Vorsprung
          gegenuber ihren Konkurrenten gewonnen haben.
        </p>
        <table onLoad={this.handleTable1} id="tableWin"></table>
        {this.renderTable1()}
        <p>
          die Wahlkreise, in denen die Partei, falls sie keinen Kreis gewonnen
          haben am knappsten verloren hat.
        </p>
        <table onLoad={this.handleTable2} id="tableLose"></table>
        {this.renderTable2()}
      </React.Fragment>
    );
  }

  handlereq1() {
    fetch("http://localhost:8000/query6_win")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableWin");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  handlereq2() {
    fetch("http://localhost:8000/query6_loser")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableLose");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  renderTable1() {
    return this.handlereq1();
  }
  renderTable2() {
    return this.handlereq2();
  }
}

export default Knappstesieger;
