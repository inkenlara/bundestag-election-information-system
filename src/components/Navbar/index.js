import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
  return (
    <>
      <Nav>
        <NavMenu>
          <NavLink to="/sitzverteilung">Sitzverteilung</NavLink>
          <NavLink to="/mitglieder">Mitglieder Bundestag</NavLink>
          <NavLink to="/wahlkreiszweit">Übersicht Wahlkreise</NavLink>
          <NavLink to="/stimmkreisSieger">Stimmkreissieger</NavLink>
          <NavLink to="/uberhangsmandate">Überhangmandate</NavLink>
          <NavLink to="/knappstesieger">Knappste Sieger</NavLink>
          <NavLink to="/wahlkreiserst">Einzelstimmen</NavLink>
          <NavLink to="/rich">Einkommen</NavLink>
          <NavLink to="/educated">Bildungsgrad</NavLink>
        </NavMenu>
      </Nav>
    </>
  );
};

export default Navbar;
