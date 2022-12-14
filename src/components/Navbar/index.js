import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
  return (
    <>
      <Nav>
        <NavMenu>
          <NavLink to="/sitzverteilung">Sitzverteilung</NavLink>
          <NavLink to="/mitglieder">Bundestag Mitglieder</NavLink>
          <NavLink to="/wahlkreiszweit">Wahlkreise Zweitstimmen</NavLink>
          <NavLink to="/stimmkreisSieger">StimmkreisSieger</NavLink>
          <NavLink to="/uberhangsmandate">Uberhangmandate</NavLink>
          <NavLink to="/knappstesieger">Knappste sieger</NavLink>
          <NavLink to="/wahlkreiserst">Wahlkreise Erststimmen</NavLink>
          <NavLink to="/rich">Rich-Poor</NavLink>
          <NavLink to="/educated">Educated-Uneducated</NavLink>
        </NavMenu>
      </Nav>
    </>
  );
};

export default Navbar;
