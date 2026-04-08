import { useAuth0 } from "@auth0/auth0-react";
import { useQueryClient } from "@tanstack/react-query";

const LogoutButton = () => {
    const { logout } = useAuth0();
    const queryClient = useQueryClient();

    return (
        <button
            onClick={() => {
                queryClient.clear();
                logout({ logoutParams: { returnTo: window.location.origin } });
            }}
            className="button logout"
        >
            Log Out
        </button>
    );
};

export default LogoutButton;
