import { useAuth0 } from "@auth0/auth0-react";
import { Button, Container } from "react-bootstrap";

function Login() {

    const { loginWithRedirect } = useAuth0();

    return (
        <Container>
            <h1>Login</h1>
            <Button onClick={() => loginWithRedirect({})}>Login</Button>
        </Container>
    );
}

export default Login;