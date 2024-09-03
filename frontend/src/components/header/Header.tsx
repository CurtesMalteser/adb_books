import './Header.css';
import Nav from 'react-bootstrap/Nav';
import { Link } from 'react-router-dom';

function NavMenu() {
  return (
    <Nav variant="pills" defaultActiveKey="home" className='justify-content-center'>
      <Nav.Item>
        <Nav.Link as={Link} to="/" eventKey="home">Home</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={Link} to="/search" eventKey="search">Search</Nav.Link>
      </Nav.Item>
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