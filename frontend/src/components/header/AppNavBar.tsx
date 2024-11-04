import Navbar from 'react-bootstrap/esm/Navbar';
import Nav from 'react-bootstrap/esm/Nav';
import Container from 'react-bootstrap/esm/Container';
import { Link } from 'react-router-dom';
import ROUTES from '../../constants/Routes';
import { useAuth0 } from '@auth0/auth0-react';
import LoginButton from '../../features/auth/LoginButton';
import { useEffect } from 'react';
import { initAuth } from '../../features/auth/authUtils';
import DarkModeToggle from '../../features/dark-mode/DarkModeToggle';
import Avatar from '../../features/user/Avatar';
import LogoutButton from '../../features/auth/LogoutButton';

function AppNavBar() {

  const auth0 = useAuth0();
  const { isAuthenticated, isLoading } = auth0;

  useEffect(() => {
    initAuth(auth0);
  }, [auth0]);

  return (
    <Navbar expand="lg" className="navbar-dark bg-primary" style={{ height: "56px", marginBottom: "48px" }} >
      <Container>
        <Nav variant="pills" defaultActiveKey="home" className='justify-content-center d-flex align-items-center'>
          <Navbar.Brand as={Link} to={ROUTES.HOME} >Book Management App</Navbar.Brand>
          <Nav.Item>
            <Nav.Link as={Link} to={ROUTES.HOME} eventKey="home">Home</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link as={Link} to={ROUTES.MY_BOOKLIST} eventKey="my-book-list">My Booklist</Nav.Link>
          </Nav.Item>
          <Avatar />
        </Nav>
        <div className="d-flex ml-auto">
          
          {!isLoading && isAuthenticated && <LogoutButton />}
          {!isLoading && !isAuthenticated && <LoginButton />}
          <DarkModeToggle />
        </div>
      </Container>
    </Navbar>
  )
}

export default AppNavBar;