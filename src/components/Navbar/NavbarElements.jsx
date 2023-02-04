import { NavLink as Link } from 'react-router-dom';
import styled from 'styled-components';

export const Nav = styled.nav`
  background: #3f51b5;
  height: 45px;
  display: flex;
  justify-content: center;
  z-index: 12;
`;

export const NavLink = styled(Link)`
  color: white;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  height: 100%;
  cursor: pointer;
  text-decoration: none;
  &.active {
    text-decoration: underline;
  }
  &:hover {
    text-decoration: underline;
  }
`;

export const NavMenu = styled.div`
  display: flex;
  justify-content: center;
  width: 100%;
  /* Second Nav */
  /* margin-right: 24px; */
  /* Third Nav */
  /* width: 100vw;
white-space: nowrap; */
  @media screen and (max-width: 768px) {
    display: none;
  }
`;
