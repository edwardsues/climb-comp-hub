import { useAuth0 } from "@auth0/auth0-react";
import { Link } from "@tanstack/react-router";
import "../../styles/navbar.scss";
import { useState } from "react";
import LoginButton from "../../auth/LoginButton";
import LogoutButton from "../../auth/LogoutButton";

function Navbar() {
    const { isAuthenticated, user } = useAuth0();
    const [menuOpen, setMenuOpen] = useState(false);

    const roles = user?.["https://climbhub.com/roles"] ?? [];
    const isGymOwner = roles.includes("gym_owner");

    return (
        <>
            {menuOpen && <div className="nav-backdrop" onClick={() => setMenuOpen(false)} />}

            <nav className="navbar">
                <div className="navbar-top">
                    <Link to="/">ClimbHub</Link>

                    <button className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
                        {menuOpen ? (
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <line x1="4" y1="4" x2="20" y2="20" />
                                <line x1="20" y1="4" x2="4" y2="20" />
                            </svg>
                        ) : (
                            <svg
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <line x1="3" y1="6" x2="21" y2="6" />
                                <line x1="3" y1="12" x2="21" y2="12" />
                                <line x1="3" y1="18" x2="21" y2="18" />
                            </svg>
                        )}
                    </button>
                </div>

                <div className={`nav-links ${menuOpen ? "open" : ""}`} onClick={() => setMenuOpen(false)}>
                    <Link to="/competitions">Competitions</Link>
                    <Link to="/calendar">Calendar</Link>
                    {isAuthenticated && <Link to="/my-competitions">My Competitions</Link>}
                    {isAuthenticated && isGymOwner && <Link to="/my-gym">My Gym</Link>}
                    {!isAuthenticated ? <LoginButton /> : <LogoutButton />}
                </div>
            </nav>
        </>
    );
}

export default Navbar;
