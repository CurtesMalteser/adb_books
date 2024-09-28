import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "react-bootstrap";

const LogoutButton = () => {
    const { logout } = useAuth0();

    const handleLogout = () => {
        logout();
    };

    return (
        <Button onClick={handleLogout}>Logout</Button>
    );
}

export default LogoutButton;