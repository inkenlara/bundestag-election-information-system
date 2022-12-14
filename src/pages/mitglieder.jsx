import React, { Component } from "react";

class Mitglieder extends Component {
  state = {};
  render() {
    return (
      <React.Fragment>
        <h2>Mitglieder des Bundestages</h2>
        <table onLoad={this.handleTable} id="tableMitglieder"></table>
        {this.renderTable()}
      </React.Fragment>
    );
  }

  handleRequest() {
    fetch("http://localhost:8000/query2_table")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableMitglieder");
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

export default Mitglieder;
