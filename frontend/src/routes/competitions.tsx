import { createFileRoute } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import type { Competition } from "../types/Competition";

export const Route = createFileRoute("/competitions")({
    component: CompetitionsComponent,
});

function CompetitionsComponent() {
    const { isPending, isError, data, error } = useQuery({
        queryKey: ["competitions"],
        queryFn: async () => {
            const response = await fetch("http://localhost:5000/api/competitions");
            if (!response.ok) {
                throw new Error("Failed to fetch competitions");
            }
            return response.json() as Promise<Competition[]>;
        },
    });

    if (isPending) {
        return <span>Loading...</span>;
    }

    if (isError) {
        return <span>Error: {error.message}</span>;
    }

    return (
        <ul>
            {data.map((competition) => (
                <li key={competition.id}>{competition.name}</li>
            ))}
        </ul>
    );
}
