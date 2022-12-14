import React, { Component } from "react";

class StimmkreisSieger extends Component {
  state = {};
  render() {
    return (
      <React.Fragment>
        <h2 id="Stimmkreissieger">Stimmkreissieger</h2>
        <table onLoad={this.handleTable} id="tableStimm"></table>
        {this.renderTable()}
      </React.Fragment>
    );
  }

  handleRequest() {
    fetch("http://localhost:8000/query4_table")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableStimm");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  renderTable() {
    return this.handleRequest();
  }
}

export default StimmkreisSieger;
