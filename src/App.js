import React from "react";
import "./App.css";
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import Home from "./pages";
import Sitzverteilung from "./pages/sitzverteilung";
import StimmkreisSieger from "./pages/stimmkreissieger";
import Wahlkreiszweit from "./pages/wahlkreiszweit";
import Mitglieder from "./pages/mitglieder";
import Uberhangsmandate from "./pages/uberhangsmandate";
import Knappstesieger from "./pages/knappstesieger";
import Wahlkreiserst from "./pages/wahlkreiserst";
import Rich from "./pages/rich";
import Educated from "./pages/educated";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Sitzverteilung />} />
        <Route path="/sitzverteilung" element={<Sitzverteilung />} />
        <Route path="/mitglieder" element={<Mitglieder />} />
        <Route path="/wahlkreiszweit" element={<Wahlkreiszweit />} />
        <Route path="/stimmkreisSieger" element={<StimmkreisSieger />} />
        <Route path="/uberhangsmandate" element={<Uberhangsmandate />} />
        <Route path="/knappstesieger" element={<Knappstesieger />} />
        <Route path="/wahlkreiserst" element={<Wahlkreiserst />} />
        <Route path="/rich" element={<Rich />} />
        <Route path="/educated" element={<Educated />} />
      </Routes>
    </Router>
  );
}

export default App;
