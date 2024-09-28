import { useAuth0 } from "@auth0/auth0-react";
import Loader from "./loader/Loader";

const Profile = () => {
    const { isLoading, isAuthenticated, user } = useAuth0();

    if (isLoading) {
        return <Loader />;
    }

    return (
        <>
            {isAuthenticated && user && (
                <div>
                    <img src={user.picture} alt={user.name} />
                    <h2>{user.name}</h2>
                    <p>{user.email}</p>
                </div>
            )}
        </>
    );
}

export default Profile;