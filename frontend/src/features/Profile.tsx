import { useAuth0 } from "@auth0/auth0-react";
import Loader from "./loader/Loader";
import Container from "react-bootstrap/esm/Container";
import TokenCard from "./user/TokenCard";
import { useAccessToken } from "./user/useAccessToken";

const Profile = () => {
    const { isLoading, isAuthenticated, user } = useAuth0();
    const token = useAccessToken();

    if (isLoading) {
        return <Loader />;
    }

    return (
        <Container style={{ marginTop: 20, marginBottom: 20, }}>
            {isAuthenticated && user && (
                <>
                    <img src={user.picture} alt={user.name} />
                    <h2>{user.name}</h2>
                    <p>{user.email}</p>
                    <TokenCard token={token} />
                </>
            )}
        </Container>
    );
}

export default Profile;