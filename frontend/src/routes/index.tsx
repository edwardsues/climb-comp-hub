import { useAuth0 } from "@auth0/auth0-react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect } from "react";
import "../styles/index.scss";
import CompetitionCard, { type Competition } from "../components/ui/CompetitionCard";

const DUMMY_COMPETITIONS: Competition[] = [
    {
        name: "Ontario Bouldering Open 2025",
        date: "April 12, 2025",
        location: "Toronto, ON",
        discipline: "Boulder",
        status: "open",
    },
    {
        name: "Rock Candy Spring Invitational",
        date: "May 3, 2025",
        location: "Ottawa, ON",
        discipline: "Boulder",
        status: "upcoming",
    },
    {
        name: "Hamilton Crusher Classic",
        date: "March 8, 2025",
        location: "Hamilton, ON",
        discipline: "Boulder",
        status: "closed",
    },
];

export const Route = createFileRoute("/")({
    component: Home,
});

function Home() {
    const { isAuthenticated, getAccessTokenSilently, loginWithRedirect } = useAuth0();

    useEffect(() => {
        if (isAuthenticated) {
            getAccessTokenSilently().then((token) => localStorage.setItem("access_token", token));
        }
    }, [isAuthenticated]);

    return (
        <div className="home-page">
            <section className="intro">
                <h1>Find comps, climb harder, and prove your sends - all in one place.</h1>
                <h2>ClimbHub is a unified platform for discovering and competing in Ontario bouldering competitions.</h2>
                <h2>All Ontario competitions in one place - no more hunting.</h2>
                {!isAuthenticated && (
                    <button className="intro-button get-started" onClick={() => loginWithRedirect()}>
                        Get Started
                    </button>
                )}
            </section>

            <section className="upcoming-comps">
                <h1>Upcoming Competitions</h1>
                <ul className="competition-cards">
                    {DUMMY_COMPETITIONS.map((comp) => (
                        <CompetitionCard key={comp.name} {...comp} />
                    ))}
                </ul>
                <Link to="/competitions" className="intro-button">
                    See all
                </Link>
            </section>

            <section className="how-it-works">
                <h1>How it works</h1>
                <div className="how-it-works-grid">
                    <div className="how-it-works-card">
                        <h2>Discover & Join</h2>
                        <p>Browse upcoming competitions across Ontario. Register and see event details all in one place.</p>
                    </div>
                    <div className="how-it-works-card">
                        <h2>Track Your Sends</h2>
                        <p>
                            Log climbs digitally during competitions - no more paper cards. Submit results and track your
                            progress.
                        </p>
                    </div>
                    <div className="how-it-works-card">
                        <h2>Host & Manage</h2>
                        <p>Create and manage competitions, handle participants, and view results seamlessly.</p>
                    </div>
                </div>
            </section>

            <section className="participating-gyms">
                <h1>Participating Gyms</h1>
                {/* TODO: add a map with gym pins */}
            </section>
        </div>
    );
}
