import { useAuth0 } from "@auth0/auth0-react";

function Navbar() {
    const { isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

    return()
}

export default Navbar;
