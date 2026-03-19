import { useAuth0 } from "@auth0/auth0-react";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/my-gym")({
    component: MyGymComponent,
});

function MyGymComponent() {
    const { isAuthenticated, isLoading, loginWithRedirect, user } = useAuth0();

    if (isLoading) return null;

    if (!isAuthenticated) {
        return (
            <div>
                <p>Sign in to see your gym</p>
                <button
                    onClick={() =>
                        loginWithRedirect({
                            appState: { returnTo: "/my-gym" },
                        })
                    }
                >
                    Sign In
                </button>
            </div>
        );
    }

    const roles = user?.["https://climbhub.com/roles"] ?? [];
    const isGymOwner = roles.includes("gym_owner");
    if (!isGymOwner) {
        return <p> You don't have access to this page.</p>;
    }

    return <div>hello "/my-gym"</div>;
}
