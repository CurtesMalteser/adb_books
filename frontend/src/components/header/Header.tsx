import './Header.css';
import Nav from 'react-bootstrap/Nav';
import { Link } from 'react-router-dom';
import ROUTES from '../../constants/Routes';

function NavMenu() {
  return (
    <Nav variant="pills" defaultActiveKey="home" className='justify-content-center'>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.HOME} eventKey="home">Home</Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as={Link} to={ROUTES.MY_BOOKLIST} eventKey="my-book-list">My Booklist</Nav.Link>
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