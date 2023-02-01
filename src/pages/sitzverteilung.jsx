import React, { Component } from 'react';

import PieChartq1 from '../components/Charts/PieChartQ1';
import PieChartq12017 from '../components/Charts/PieChartQ1_2017';

class Sitzverteilung extends Component {
  state = {
    data: {},
    url: 'http://localhost:8000/query1_chart',
    is2021: true,
  };

  handleDisplay() {
    var chec = document.getElementsByName('year-mit');
    if (chec[0].checked) {
      this.setState({ is2021: true });
    } else {
      this.setState({ is2021: false });
    }
  }

  render() {
    return (
      <React.Fragment>
        <h2 /*onLoad={this.handleRequestNew}*/>Sitzverteilung</h2>
        {/*this.handleRequestNew()*/}
        {/*console.log(this.state.data)*/}
        <form>
          <div>
            <input
              type="radio"
              name="year-mit"
              id="y2021"
              value="2021"
              defaultChecked
            />
            <label htmlFor="y2021">2021</label>

            <input type="radio" name="year-mit" id="y2017" value="2017" />
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
        <div>{this.state.is2021 ? <PieChartq1 /> : <PieChartq12017 />}</div>
        <table
          onLoad={
            this.state.is2021 ? this.renderTable() : this.renderTable2017()
          }
          id="tableSitze"
        ></table>
        {this.state.is2021 ? this.renderTable() : this.renderTable2017()}
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
    fetch('http://localhost:8000/query1_table')
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById('tableSitze');
        tag_id.innerHTML = data['data'];
        return data['data'];
      })
      .catch(function (err) {
        console.log('Fetch Error :-S', err);
      });
  }

  renderTable() {
    return this.handleRequest();
  }

  handleRequest2017() {
    fetch('http://localhost:8000/query1_table2017')
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById('tableSitze');
        tag_id.innerHTML = data['data'];
        return data['data'];
      })
      .catch(function (err) {
        console.log('Fetch Error :-S', err);
      });
  }

  renderTable2017() {
    return this.handleRequest2017();
  }
}

export default Sitzverteilung;
