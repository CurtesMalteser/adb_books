import Navbar from 'react-bootstrap/Navbar';
import { Container } from "react-bootstrap";
import ROUTES from "../constants/Routes";

// Make a generic navbar component and just display on this error page,
// the rest add children content
function ErrorNavbar() {
    return (
        <Navbar bg="primary" variant="light">
            <Container>
                <Navbar.Brand href={ROUTES.HOME}>Bookshelf</Navbar.Brand>
            </Container>
        </Navbar>
    )
}

function ErrorPage() {
    return (
        <>

            <ErrorNavbar />
            <div style={{
                margin: '2rem auto',
                textAlign: 'center',
            }}>
                <h1>An Error occurre!</h1>
                <p>🚨 Could not find this page! 🚨</p>
                <a href={ROUTES.HOME}>Go back to the home page</a>
            </div>
        </>
    )
}

export default ErrorPage;