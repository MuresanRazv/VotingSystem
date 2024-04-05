from models.vote import Vote
from paillier import encrypt
from crud import create_vote as create_vote_crud, get_poll_by_id, get_votes_by_user_id
from fastapi import HTTPException

async def create_vote(user_id: str, poll_id: str, newVote: Vote):
    poll = await get_poll_by_id(poll_id)

    # check if user already voted
    votes = await get_votes_by_user_id(str(user_id))
    if votes is not None:
        for vote in votes:
            if str(poll_id) == str(vote.poll_id) and str(vote.user_id) == str(user_id):
                raise HTTPException(status_code=400, detail="User already voted")

    # encrypt tallies
    for candidate in newVote.candidates:
        candidate.tally = str(await encrypt(eval(poll.encryption_key), int(candidate.tally)))

    return await create_vote_crud(newVote)
    