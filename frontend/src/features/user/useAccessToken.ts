import { useAuth0 } from "@auth0/auth0-react";
import { useEffect, useState } from "react";

export const useAccessToken = () => {
    const { isAuthenticated, getAccessTokenSilently } = useAuth0();
    const [token, setToken] = useState<string | null>(null);

    useEffect(() => {
        const fetchToken = async () => {
            if (isAuthenticated) {
                try {
                    const token = await getAccessTokenSilently();
                    setToken(token);
                } catch (error) {
                    console.error("Error fetching access token:", error);
                }
            }
        };

        fetchToken();
    }, [isAuthenticated, getAccessTokenSilently]);

    return token;
};