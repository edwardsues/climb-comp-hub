import { useAuth0 } from "@auth0/auth0-react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";
import Profile from "../auth/Profile";
import LogoutButton from "../auth/LogoutButton";
import LoginButton from "../auth/LoginButton";

export const Route = createFileRoute("/")({
    component: Home,
});

function Home() {
    const { isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

    useEffect(() => {
        if (isAuthenticated) {
            getAccessTokenSilently().then((token) => localStorage.setItem("access_token", token));
        }
    }, [isAuthenticated]);

    if (isLoading) {
        return (
            <div className="app-container">
                <div className="loading-state">
                    <div className="loading-text">Loading...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="app-container">
                <div className="error-state">
                    <div className="error-title">Oops!</div>
                    <div className="error-message">Something went wrong</div>
                    <div className="error-sub-message">{error.message}</div>
                </div>
            </div>
        );
    }

    return (
        <div className="app-container">
            <div className="main-card-wrapper">
                {isAuthenticated ?? (
                    <div className="logged-in-section">
                        <div className="logged-in-message">✅ Successfully authenticated!</div>
                        <h2 className="profile-section-title">Your Profile</h2>
                        <div className="profile-card">
                            <Profile />
                        </div>
                        <LogoutButton />
                    </div>
                )}
            </div>
        </div>
    );
}
