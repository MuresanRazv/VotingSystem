from crud import create_poll as create_poll_crud, create_candidate as create_candidate_crud, create_poll_candidate as create_poll_candidate_crud, get_poll_by_id, get_votes_by_user_id, get_user_by_id, update_user
from models import Poll, Candidate, UpdatedPoll, Vote
import paillier as Paillier
from fastapi import HTTPException
from datetime import datetime

async def create_poll(poll_data: UpdatedPoll, user_id: str):
    poll_obj = Poll(**poll_data.model_dump())
    
    # create encryption/decryption keys
    public_key, private_key = await Paillier.generate_keys()

    # encrypt candidate votes count (initially 0)
    if not poll_obj.candidates is None:
        for candidate_id in poll_obj.candidates:
            poll_obj.candidates[candidate_id] = await Paillier.encrypt(public_key, 0)

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

async def create_poll_candidate(poll_id: str, candidate: Candidate):
    await create_candidate_crud(candidate)
    poll = await get_poll_by_id(poll_id)
    public_key = eval(poll.encryption_key)

    # empty count
    encrypted_count = await Paillier.encrypt(public_key, 0)

    # add candidate to the poll
    return await create_poll_candidate_crud(poll_id, candidate.id, encrypted_count)

async def update_poll_candidate(poll_id: str, candidate_id: str, poll: UpdatedPoll):
    return await update_poll_candidate(poll_id, candidate_id, poll)

async def add_vote(poll_id: str, vote: Vote, user_id: str):
    # check if user already voted
    votes = await get_votes_by_user_id(user_id, poll_id)
    if votes is not None:
        for vote in votes:
            if vote.user_id == user_id:
                raise HTTPException(status_code=400, detail="User already voted")
    
    poll = await get_poll_by_id(poll_id)
    public_key = eval(poll.encryption_key)

    # add vote
    if poll.candidates is not None:
        public_key = eval(poll.encryption_key)
        for (candidate_id, count) in vote.candidates.items():
            poll.candidates[candidate_id] = str(await Paillier.add(public_key, int(count), int(poll.candidates[candidate_id])))
    
        await update_poll_candidate(poll_id, candidate_id, poll)