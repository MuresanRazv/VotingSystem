import type { Vote } from "../stores/votes";
import { PUBLIC_BASE_API_URL } from "$env/static/public";

async function addVote(poll_id: string, vote: Vote) {
    // Clear candidates id's
    vote.candidates = vote.candidates.map(candidate => {
        return {
            name: candidate.name,
            description: candidate.description,
            tally: candidate.tally
        }
    });

    return await fetch(PUBLIC_BASE_API_URL + `/votes/${poll_id}/vote`, {
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

async function getUserVotes(user_id: string) {
    return await fetch(PUBLIC_BASE_API_URL + `/votes/${user_id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch user votes');
        }

        return response.json();
    })
    .catch(error => {
        window.location.href = '/login';
    });
}

export { addVote, getUserVotes };