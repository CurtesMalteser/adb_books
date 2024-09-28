import { Auth0ContextInterface } from '@auth0/auth0-react';
/**
 * This module provides an abstraction layer for handling Auth0 authentication outside of UI components.
 * It allows other parts of the application (such as utility functions or API services) to access the current Auth0 access token without directly
 * using the Auth0 React hooks in the UI components.
 * 
 * This approach centralizes token management and separates authentication logic from UI components, promoting cleaner code and better reusability.
 */

/**
 * Stores the getAccessTokenSilently method from Auth0.
 */
let getAccessToken: Auth0ContextInterface['getAccessTokenSilently'] | null = null;

/**
 * Initializes the authentication mechanism by storing the getAccessTokenSilently method from Auth0 in a local variable.
 * @param auth0 : Auth0ContextInterface
 */
export const initAuth = (auth0: Auth0ContextInterface) => {
    const { getAccessTokenSilently } = auth0;
    getAccessToken = getAccessTokenSilently;
};

/**
 * Returns the current access token by calling the stored getAccessTokenSilently method. Throws an error if Auth0 is not initialized.
 * @returns Promise<string>
 */
export const fetchAccessToken = async () => {
    if (!getAccessToken) {
        throw new Error('Auth0 is not initialized');
    }

    return getAccessToken();
};