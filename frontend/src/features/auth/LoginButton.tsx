import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "react-bootstrap";
import ROUTES from "../../constants/Routes";
import { useLocation } from "react-router-dom";

const LoginButton = () => {
    const { loginWithRedirect } = useAuth0();
    const location = useLocation();

    const handleSignUp = async () => {
      const returnTo = location.state?.path || ROUTES.HOME;

      await loginWithRedirect({
        appState: {
          returnTo: returnTo,
        },
        authorizationParams: {
          screen_hint: "signup",
        },
      });
    };

    return (
        <Button onClick={handleSignUp}>Log In</Button>
    );
}

export default LoginButton;