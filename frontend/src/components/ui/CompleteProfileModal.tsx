import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import "../../styles/modal.scss";

type Props = {
    onComplete: () => void;
};

type ProfileUpdate = {
    name: string;
    dob: string;
};

function CompleteProfileModal({ onComplete }: Props) {
    const [name, setName] = useState("");
    const [dob, setDob] = useState("");

    const mutation = useMutation({
        mutationFn: async (data: ProfileUpdate) => {
            const token = localStorage.getItem("access_token");
            const res = await fetch("http://localhost:5000/api/users/me", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(data),
            });
            if (!res.ok) throw new Error("Failed to update profile");
            return res.json();
        },
        onSuccess: () => onComplete(),
    });

    return (
        <div className="modal-backdrop">
            <div className="modal">
                <header>
                    <h1>Let's create your account.</h1>
                    <span>This is information required to register for competitions.</span>
                </header>

                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        mutation.mutate({ name, dob });
                    }}
                >
                    <label htmlFor="name">Name</label>
                    <input name="name" value={name} onChange={(e) => setName(e.target.value)} required />
                    <label htmlFor="dob">Date of birth</label>
                    <input name="dob" type="date" value={dob} onChange={(e) => setDob(e.target.value)} required />
                    <button type="submit" className="btn-primary" disabled={mutation.isPending}>
                        {mutation.isPending ? "Saving..." : "Save"}
                    </button>
                    {mutation.isError && <span className="errorText">Unable to complete profile. Please try again.</span>}
                </form>
            </div>
        </div>
    );
}

export default CompleteProfileModal;
