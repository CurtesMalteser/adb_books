import './Header.css';
import Nav from 'react-bootstrap/Nav';
import { Link } from 'react-router-dom';
import ROUTES from '../../constants/Routes';
import { useAuth0 } from '@auth0/auth0-react';
import LogoutButton from '../../features/auth/LogoutButton';
import LoginButton from '../../features/auth/LoginButton';

function NavMenu() {

  const { isAuthenticated } = useAuth0();

  return (
    <Nav variant="pills" defaultActiveKey="home" className='justify-content-center'>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.HOME} eventKey="home">Home</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.MY_BOOKLIST} eventKey="my-book-list">My Booklist</Nav.Link>
      </Nav.Item>
      {isAuthenticated && (<LogoutButton />)}
      {!isAuthenticated && (<LoginButton />)}
    </Nav>
  )
}

function Header() {
  return (
    <header>
      <h1>Book Management App</h1>
      <NavMenu />
    </header>
  );
}

export default Header;