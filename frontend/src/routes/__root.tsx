import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import Navbar from "../components/layout/Navbar";
import { useAuth0 } from "@auth0/auth0-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import CompleteProfileModal from "../components/ui/CompleteProfileModal";

export const Route = createRootRoute({
    component: RootComponent,
    notFoundComponent: () => <div>404 Not Found</div>,
});

function RootComponent() {
    const { isAuthenticated, getAccessTokenSilently } = useAuth0();
    const { data } = useQuery({
        queryKey: ["profile"],
        queryFn: async () => {
            const token = await getAccessTokenSilently();
            const res = await fetch("http://localhost:5000/api/users/me", {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (!res.ok) throw new Error("Failed to fetch profile");
            return res.json();
        },
        enabled: isAuthenticated,
    });

    const profileIncomplete = !!data && !data.name;
    const queryClient = useQueryClient();

    return (
        <>
            <Navbar />
            {profileIncomplete && (
                <CompleteProfileModal onComplete={() => queryClient.invalidateQueries({ queryKey: ["profile"] })} />
            )}
            <Outlet />
            <TanStackRouterDevtools />
        </>
    );
}
