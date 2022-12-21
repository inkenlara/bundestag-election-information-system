import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
/* root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); */ // Removed strict mode because react calls the API two times per request then and makes it slower
