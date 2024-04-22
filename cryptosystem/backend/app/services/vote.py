from models.vote import Vote, Poll, ResponseVote
from paillier import encrypt
from crud import create_vote as create_vote_crud, get_poll_by_id, get_votes_by_user_id as get_votes_by_user_id_crud
from fastapi import HTTPException

async def create_vote(user_id: str, poll_id: str, newVote: Vote):
    poll = await get_poll_by_id(poll_id)

    # check if user already voted
    if (await user_voted(user_id, poll_id)):
        raise HTTPException(status_code=400, detail="User already voted")

    # encrypt tallies
    for candidate in newVote.candidates:
        candidate.tally = str(await encrypt(eval(poll.encryption_key), int(candidate.tally)))

    return await create_vote_crud(newVote)
    
async def get_votes_by_user_id(user_id: str):
    votes = await get_votes_by_user_id_crud(user_id)

    if votes is None:
        return []
    
    responseVotes = []
    for vote in votes:
        poll = await get_poll_by_id(vote.poll_id)
        responseVotes.append(ResponseVote(poll=poll))

    return responseVotes

async def user_voted(user_id: str, poll_id: str):
    # check if user already voted
    votes = await get_votes_by_user_id_crud(str(user_id))
    if votes is not None:
        for vote in votes:
            if str(poll_id) == str(vote.poll_id) and str(vote.user_id) == str(user_id):
                return True
            
    return False