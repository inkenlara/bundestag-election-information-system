import React, { Component } from "react";
import PieChartRich from "../components/Charts/PieChartRich";
import PieChartPoor from "../components/Charts/PieChartPoor";

class Rich extends Component {
  state = {
    url1: "http://localhost:8000/query8_rich",
    url2: "http://localhost:8000/query8_poor",
  };
  render() {
    return (
      <React.Fragment>
        <h2 id="RichPoor">
          Durchschnitt der top 5 Parteien in den 10 reichsten und den 10 ärmsten
          Wahlkreisen
        </h2>
        <div>
          <div id="query8-reich">
            <PieChartRich />
          </div>
          <div id="query8-arm">
            <PieChartPoor />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default Rich;
