from crud import create_poll
from models import Poll, CreatePoll
from paillier import Paillier
from datetime import datetime

async def create_poll(poll_data: CreatePoll):
    poll_obj = Poll(**poll_data.model_dump())
    
    # create encryption/decryption keys
    paillier = Paillier()
    public_key, private_key = paillier.generate_keys()

    # encrypt candidate votes count (initially 0)
    for candidate_id in poll_obj.candidates:
        poll_obj.candidates[candidate_id] = paillier.encrypt(public_key, 0)

    # set encryption key
    poll_obj.encryption_key = public_key

    poll_obj.created_at = datetime.now()
    poll_obj.updated_at = datetime.now()

    # create the poll
    await create_poll(poll_obj)

    # return private key to the user
    return private_key