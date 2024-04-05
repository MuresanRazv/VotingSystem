import type { Vote } from "../stores/votes";

async function addVote(poll_id: string, vote: Vote) {
    // Clear candidates id's
    vote.candidates = vote.candidates.map(candidate => {
        return {
            name: candidate.name,
            description: candidate.description,
            tally: candidate.tally
        }
    });

    return await fetch(`http://localhost:8000/api/votes/${poll_id}/vote`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({
            poll_id: vote.poll_id,
            user_id: vote.user_id,
            candidates: vote.candidates
        }),
    });

}

export { addVote };