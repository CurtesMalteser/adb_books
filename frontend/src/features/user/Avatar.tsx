import { useAuth0 } from "@auth0/auth0-react";
import Image from "react-bootstrap/esm/Image";
import Nav from "react-bootstrap/esm/Nav";
import { Link } from "react-router-dom";
import ROUTES from "../../constants/Routes";
import './Avatar.css';

const Avatar = ({ children }: { children?: React.ReactNode; }) => {
    const { user } = useAuth0();

    return (
        <>
            {user &&
                <Nav.Item>
                    <Nav.Link as={Link} to={ROUTES.PROFILE} eventKey="profile">
                        <Image className="avatar-image"
                            src={user.picture}
                            alt={`Profile Picture ${user.name}`}
                            roundedCircle />
                        {children && <span className="avatar-text">{children}</span>}
                    </Nav.Link>
                </Nav.Item>
            }
        </>
    );
}

export default Avatar;