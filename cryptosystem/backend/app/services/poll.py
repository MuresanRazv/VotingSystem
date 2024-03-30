from crud import create_poll, create_candidate, create_poll_candidate, get_poll_by_id, get_votes_by_user_id
from models import Poll, Candidate, UpdatedPoll, Vote
from paillier import Paillier
from fastapi import HTTPException
from datetime import datetime

async def create_poll(poll_data: UpdatedPoll):
    poll_obj = Poll(**poll_data.model_dump())
    
    # create encryption/decryption keys
    paillier = Paillier()
    public_key, private_key = paillier.generate_keys()

    # encrypt candidate votes count (initially 0)
    for candidate_id in poll_obj.candidates:
        poll_obj.candidates[candidate_id] = paillier.encrypt(public_key, 0)

    # set encryption key
    poll_obj.encryption_key = str(public_key)

    poll_obj.created_at = datetime.now()
    poll_obj.updated_at = datetime.now()

    # create the poll
    await create_poll(poll_obj)

    # return private key to the user
    return str(private_key)

async def create_poll_candidate(poll_id: str, candidate: Candidate):
    await create_candidate(candidate)
    poll = await get_poll_by_id(poll_id)
    paillier = Paillier()
    public_key = int(poll.encryption_key)

    # empty count
    encrypted_count = paillier.encrypt(public_key, 0)

    # add candidate to the poll
    return await create_poll_candidate(poll_id, candidate.id, encrypted_count)

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
    paillier = Paillier()
    public_key = int(poll.encryption_key)

    # add vote
    if poll.candidates is not None:
        paillier = Paillier()
        public_key = poll.encryption_key
        for (candidate_id, count) in vote.candidates.items():
            poll.candidates[candidate_id] = str(paillier.add(public_key, int(count), int(poll.candidates[candidate_id])))
    
        await update_poll_candidate(poll_id, candidate_id, poll)