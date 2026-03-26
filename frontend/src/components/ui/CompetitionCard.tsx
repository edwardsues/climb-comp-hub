import "../../styles/competition-card.scss";

export type Competition = {
    name: string;
    date: string;
    location: string;
    discipline: string;
    status: "open" | "closed" | "upcoming";
};

// TODO: add onClick functionality that will then  navigate them to the competition page
function CompetitionCard({ name, date, location, discipline, status }: Competition) {
    return (
        <li className="competition-card">
            <header>
                <span className={`status-badge ${status}`}>{status}</span>
                <span className="discipline">{discipline}</span>
            </header>
            <h3 className="name">{name}</h3>
            <div className="details">
                <p>{date}</p>
                <p>{location}</p>
            </div>
        </li>
    );
}

export default CompetitionCard;
