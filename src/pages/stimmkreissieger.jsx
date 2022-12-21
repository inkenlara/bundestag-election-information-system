import React, { Component } from "react";

class StimmkreisSieger extends Component {
  state = {};
  render() {
    return (
      <React.Fragment>
        <h2 id="Stimmkreissieger">Stimmkreissieger</h2>
        <form>
          <div>
            <input
              type="radio"
              name="year-stimm"
              id="y2021"
              value="2021"
              defaultChecked
            />
            <label htmlFor="y2021">2021</label>

            <input type="radio" name="year-stimm" id="y2017" value="2017" />
            <label htmlFor="y2017">2017</label>
          </div>
        </form>

        <button
          type="text"
          className="choose-year"
          onClick={() => {
            this.handleDisplay();
          }}
        >
          Choose
        </button>
        <table id="tableStimm"></table>
      </React.Fragment>
    );
  }

  handleDisplay() {
    var chec = document.getElementsByName("year-stimm");
    if (chec[0].checked) this.renderTable();
    else this.renderTable2017();
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

  handleRequest2017() {
    fetch("http://localhost:8000/query4_table2017")
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

  renderTable2017() {
    return this.handleRequest2017();
  }
}

export default StimmkreisSieger;
