import { useAuth0 } from "@auth0/auth0-react";
import Button from "react-bootstrap/esm/Button";
import Image from "react-bootstrap/esm/Image";
import { useNavigate } from "react-router-dom";
import ROUTES from "../../constants/Routes";

const LogoutButton = () => {
    const { logout, user } = useAuth0();
    const navigate = useNavigate();


    return (
        <>
            {user &&
                <div
                    className="d-flex"
                    style={{ marginRight: '24px' }}
                    onClick={() => navigate(ROUTES.PROFILE)}>
                    <Image style={{ width: '50px', height: '50px', marginRight: '10px' }}
                        src={user.picture}
                        alt={`Profile Picture ${user.name}`}
                        roundedCircle />
                </div>}
            <Button onClick={() => logout()}>Logout</Button>
        </>
    );
}

export default LogoutButton;