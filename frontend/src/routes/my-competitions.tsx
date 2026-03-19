import { useAuth0 } from "@auth0/auth0-react";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/my-competitions")({
    component: MyCompetitionsComponent,
});

function MyCompetitionsComponent() {
    const { isAuthenticated, isLoading, loginWithRedirect } = useAuth0();

    if (isLoading) return null;

    if (!isAuthenticated) {
        return (
            <div>
                <p>Sign in to see your competitions</p>
                <button
                    onClick={() =>
                        loginWithRedirect({
                            appState: { returnTo: "/my-competitions" },
                        })
                    }
                >
                    Sign In
                </button>
            </div>
        );
    }

    return <div>Hello "/my-competitions"!</div>;
}
