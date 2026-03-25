import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import Navbar from "../components/layout/Navbar";
import "../styles/root.scss";

export const Route = createRootRoute({
    component: RootComponent,
    notFoundComponent: () => <div>404 Not Found</div>,
});

function RootComponent() {
    return (
        <>
            <Navbar />
            <Outlet />
            <TanStackRouterDevtools />
        </>
    );
}
