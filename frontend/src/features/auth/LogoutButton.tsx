import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/esm/Button";

const LogoutButton = () => {
    const { logout, user } = useAuth0();
    return (
        <Button onClick={() => logout()}>Logout</Button>
    );
}

export default LogoutButton;