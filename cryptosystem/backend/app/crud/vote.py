from database.connection import client_db
from models import Vote
from bson import ObjectId
from fastapi import HTTPException


async def create_vote(vote: Vote) -> Vote:
    vote_dict = vote.model_dump()
    inserted_vote = await client_db.votes.insert_one(vote_dict)
    vote._id = inserted_vote.inserted_id
    return vote

async def get_votes_by_poll_id(poll_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"poll_id": ObjectId(poll_id)}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_votes_by_user_id(user_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"user_id": ObjectId(user_id)}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_vote_by_id(vote_id: str) -> Vote:
    vote_dict = await client_db.votes.find_one({"_id": ObjectId(vote_id)})
    if (vote_dict is None):
        return None
    return Vote(**vote_dict)

async def delete_vote(vote_id: str):
    await client_db.votes.delete_one({"_id": ObjectId(vote_id)})

async def delete_votes_by_poll_id(poll_id: str):
    await client_db.votes.delete_many({"poll_id": ObjectId(poll_id)})

async def delete_votes_by_user_id(user_id: str):
    await client_db.votes.delete_many({"user_id": ObjectId(user_id)})

async def update_vote(vote_id: str, vote: Vote) -> Vote:
    vote_dict = vote.model_dump()

    try:
        result = await client_db.votes.update_one({"_id": ObjectId(vote_id)}, {"$set": vote_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Vote not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating vote")

    return await get_vote_by_id(vote_id)