import Offcanvas from "react-bootstrap/esm/Offcanvas";
import Nav from "react-bootstrap/esm/Nav";
import { Link } from "react-router-dom";
import ROUTES from "../../constants/Routes";
import { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { initAuth } from "../../features/auth/authUtils";
import LogoutButton from "../../features/auth/LogoutButton";
import LoginButton from "../../features/auth/LoginButton";
import DarkModeToggle from "../../features/dark-mode/DarkModeToggle";
import { Button, Container, Navbar } from "react-bootstrap";
import { ReactComponent as Menu } from '../../assets/svg/menu.svg';

function OffcanvasMenu({ show, handleClose }: { show: boolean, handleClose: () => void }) {

    const auth0 = useAuth0();
    const { isAuthenticated, isLoading } = auth0;

    useEffect(() => {
        initAuth(auth0);
    }, [auth0]);

    return (
        <Offcanvas show={show} onHide={handleClose}>
            <Offcanvas.Header closeButton>
                <Offcanvas.Title>Book Management App</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
                <Nav variant="pills" defaultActiveKey="home" className='flex-column'>
                    <Nav.Link as={Link} to={ROUTES.HOME} eventKey="home">Home</Nav.Link>
                    <Nav.Link as={Link} to={ROUTES.MY_BOOKLIST} eventKey="my-book-list">My Booklist</Nav.Link>
                </Nav>
                <div className="d-flex ml-auto">
                    {!isLoading && isAuthenticated && <LogoutButton />}
                    {!isLoading && !isAuthenticated && <LoginButton />}
                    <DarkModeToggle />
                </div>
            </Offcanvas.Body>
        </Offcanvas>
    );
}

function MobileNavBar() {

    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return (
        <>
            <Navbar expand="lg" className="navbar-dark bg-primary" style={{ marginBottom: "48px"}} >
                <Container className="d-flex">
                    <Button onClick={handleShow} style={{ marginRight: "8px", padding:0}}>
                        <Menu />
                    </Button>
                    <Navbar.Brand className="me-auto"
                        as={Link} to={ROUTES.HOME} >Book Management App</Navbar.Brand>
                </Container>
            </Navbar>
            <OffcanvasMenu show={show} handleClose={handleClose} />
        </>
    );
}

export default MobileNavBar;