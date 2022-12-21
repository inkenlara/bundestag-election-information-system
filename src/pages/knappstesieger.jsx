import React, { Component } from "react";

class Knappstesieger extends Component {
  state = {};
  render() {
    return (
      <React.Fragment>
        <h2 id="knappste">Knappste Sieger</h2>
        <form>
          <div>
            <input
              type="radio"
              name="year-knapp"
              id="y2021"
              value="2021"
              defaultChecked
            />
            <label htmlFor="y2021">2021</label>

            <input type="radio" name="year-knapp" id="y2017" value="2017" />
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

        <p>
          die gewählten Erstkandidaten, welche mit dem geringsten Vorsprung
          gegenuber ihren Konkurrenten gewonnen haben.
        </p>
        <table id="tableWin"></table>
        <p>
          die Wahlkreise, in denen die Partei, falls sie keinen Kreis gewonnen
          haben am knappsten verloren hat.
        </p>
        <table id="tableLose"></table>
      </React.Fragment>
    );
  }

  handleDisplay() {
    var chec = document.getElementsByName("year-knapp");
    if (chec[0].checked) {
      this.renderTable1();
      this.renderTable2();
    } else {
      this.renderTable12017();
      this.renderTable22017();
    }
  }

  handlereq12017() {
    fetch("http://localhost:8000/query6_win2017")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableWin");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  handlereq1() {
    fetch("http://localhost:8000/query6_win")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableWin");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  handlereq22017() {
    fetch("http://localhost:8000/query6_loser2017")
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableLose");
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
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("tableLose");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }

  renderTable12017() {
    return this.handlereq12017();
  }
  renderTable22017() {
    return this.handlereq22017();
  }

  renderTable1() {
    return this.handlereq1();
  }
  renderTable2() {
    return this.handlereq2();
  }
}

export default Knappstesieger;
