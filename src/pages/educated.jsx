import React, { Component } from "react";
import PieChartHigh from "../components/Charts/PieChartHigh";
import PieChartLow from "../components/Charts/PieChartLow";

class Educated extends Component {
  state = {
    url1: "http://localhost:8000/query9_high",
    url2: "http://localhost:8000/query9_low",
  };
  render() {
    return (
      <React.Fragment>
        <h2 id="Add2">
          Durchschnitt der Top Parteien in den 10 gebildetsten und den 10
          ungebildetsten Wahlkreisen
        </h2>
        <div>
          <div id="query9-high">
            <PieChartHigh />
          </div>
          <div id="query9-low">
            <PieChartLow />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Educated;
