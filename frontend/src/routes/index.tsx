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
    const { isAuthenticated, getAccessTokenSilently } = useAuth0();

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
            </section>

            <section className="upcoming-comps">
                <h1>Upcoming Competitions</h1>
                <ul className="competition-cards">
                    {DUMMY_COMPETITIONS.map((comp) => (
                        <CompetitionCard key={comp.name} {...comp} />
                    ))}
                </ul>
                <Link to="/competitions" className="see-all">
                    See all
                </Link>
            </section>

            <section className="participating-gyms">
                <h1>Participating Gyms</h1>
                {/* TODO: add a map with gym pins */}
            </section>
        </div>
    );
}
