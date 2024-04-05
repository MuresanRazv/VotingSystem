from crud import create_poll as create_poll_crud, get_poll_by_id, get_votes_by_user_id, get_user_by_id, update_user, update_poll as update_poll_crud, delete_poll as delete_poll_crud
from models import Poll, Candidate, Vote
from paillier import add, generate_keys, encrypt
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

async def create_poll(poll_data: Poll, user_id: str):
    poll_obj = Poll(**poll_data.model_dump())
    
    # create encryption/decryption keys
    public_key, private_key = await generate_keys()

    # encrypt candidate votes count (initially 0)
    if not poll_obj.candidates is None:
        for candidate in poll_obj.candidates:
            candidate.tally = str(await encrypt(public_key, 0))

    # set encryption key
    poll_obj.encryption_key = str(public_key)

    poll_obj.created_at = datetime.now()
    poll_obj.updated_at = datetime.now()
    poll_obj.created_by = user_id

    # create the poll
    await create_poll_crud(poll_obj)

    # set private key for user
    user = await get_user_by_id(user_id)
    if user.polls is None:
        user.polls = {}
    user.polls[str(poll_obj.id)] = str(private_key)

    # update user with private key
    await update_user(str(user_id), user)

async def update_poll(poll_id: str, poll_data: Poll):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    poll.title = poll_data.title
    poll.description = poll_data.description
    poll.candidates = poll_data.candidates
    poll.is_private = poll_data.is_private
    poll.multiple_choice = poll_data.multiple_choice
    for candidate in poll.candidates:
        if (candidate.tally is None):
            candidate.tally = str(await encrypt(eval(poll.encryption_key), 0))
    
    poll.updated_at = datetime.now()

    return await update_poll_crud(poll_id, poll)

async def add_vote(poll_id: str, vote: Vote, user_id: str):
    poll = await get_poll_by_id(poll_id)
    public_key = eval(poll.encryption_key)

    # add vote
    if poll.candidates is not None:
        public_key = eval(poll.encryption_key)
        for voteCandidate, pollCandidate in zip(vote.candidates, poll.candidates):
            pollCandidate.tally = str(await add(public_key, int(pollCandidate.tally), int(voteCandidate.tally)))

    await update_poll_crud(poll_id, poll)

async def delete_poll(poll_id: str):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")

    return await delete_poll_crud(poll_id)