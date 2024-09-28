import './Header.css';
import Nav from 'react-bootstrap/Nav';
import { Link, useNavigate } from 'react-router-dom';
import ROUTES from '../../constants/Routes';
import { useAuth0 } from '@auth0/auth0-react';
import LogoutButton from '../../features/auth/LogoutButton';
import LoginButton from '../../features/auth/LoginButton';
import { useEffect } from 'react';
import { initAuth } from '../../features/auth/authUtils';
import { Button } from 'react-bootstrap';

function LogoutMenu() {
  const navigate = useNavigate();
  return (<>
    <Button onClick={() => navigate(ROUTES.PROFILE)}>Profile</Button>
    <LogoutButton />
  </>)
}

function NavMenu() {

  const auth0 = useAuth0();
  const { isAuthenticated } = auth0;

  useEffect(() => {
    initAuth(auth0);
  }, [auth0]);

  return (
    <Nav variant="pills" defaultActiveKey="home" className='justify-content-center'>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.HOME} eventKey="home">Home</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.MY_BOOKLIST} eventKey="my-book-list">My Booklist</Nav.Link>
      </Nav.Item>
      {isAuthenticated && (<LogoutMenu />)}
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