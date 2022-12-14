import React, { Component } from "react";
// import { Bar } from "react-chartjs-2";
import BarChart from "../components/Charts/BarChart";

class Sitzverteilung extends Component {
  state = {
    data: {},
    url: "http://localhost:8000/query1_chart",
  };
  render() {
    return (
      <React.Fragment>
        <h2 /*onLoad={this.handleRequestNew}*/>Sitzverteilung</h2>
        {/*this.handleRequestNew()*/}
        {/*console.log(this.state.data)*/}
        <div>
          <BarChart /*data={this.state.data}*/ /* options={ } */ />
        </div>
        <table onLoad={this.handleTable} id="tableSitze"></table>
        {this.renderTable()}
      </React.Fragment>
    );
  }

  /*   handleRequestNew = () => {
    fetch("http://localhost:8000/query1_chart")
      .then(function (response) {
        return response.json();
      })
      .then(function (data_rec) {
        this.setState({
          data: data_rec,
        });
        console.log(data_rec);
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }; */

  handleRequest() {
    fetch("http://localhost:8000/query1_table")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableSitze");
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

export default Sitzverteilung;
