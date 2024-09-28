import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "react-bootstrap";
import ROUTES from "../../constants/Routes";

const LoginButton = () => {
    const { loginWithRedirect } = useAuth0();

    const handleSignUp = async () => {
      await loginWithRedirect({
        appState: {
          returnTo: ROUTES.MY_BOOKLIST,
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