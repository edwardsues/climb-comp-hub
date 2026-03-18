import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/competitions")({
    component: CompetitionsComponent,
});

function CompetitionsComponent() {
    return <div>Hello "/competitions"!</div>;
}
