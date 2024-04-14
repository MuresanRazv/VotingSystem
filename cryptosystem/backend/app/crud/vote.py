from database.connection import client_db
from models import Vote
from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime, timedelta

async def create_vote(vote: Vote) -> Vote:
    vote_dict = vote.model_dump()
    vote_dict["created_at"] = datetime.now()
    inserted_vote = await client_db.votes.insert_one(vote_dict)
    return await get_vote_by_id(str(inserted_vote.inserted_id))

async def get_votes_by_poll_id(poll_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"poll_id": str(poll_id)}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_votes_by_user_id(user_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"user_id": str(user_id)}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_vote_by_poll_and_user_id(poll_id: str, user_id: str) -> Vote:
    vote_dict = await client_db.votes.find_one({"poll_id": str(poll_id), "user_id": str(user_id)})
    if (vote_dict is None):
        return None
    return Vote(**vote_dict)

async def get_vote_by_id(vote_id: str) -> Vote:
    vote_dict = await client_db.votes.find_one({"_id": ObjectId(vote_id)})
    if (vote_dict is None):
        return None
    return Vote(**vote_dict)

async def delete_vote(vote_id: str):
    await client_db.votes.delete_one({"_id": ObjectId(vote_id)})

async def delete_votes_by_poll_id(poll_id: str):
    await client_db.votes.delete_many({"poll_id": str(poll_id)})

async def delete_votes_by_user_id(user_id: str):
    await client_db.votes.delete_many({"user_id": str(user_id)})

async def update_vote(vote_id: str, vote: Vote) -> Vote:
    vote_dict = vote.model_dump()

    try:
        result = await client_db.votes.update_one({"_id": ObjectId(vote_id)}, {"$set": vote_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Vote not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating vote")

    return await get_vote_by_id(vote_id)

async def get_weekly_votes() -> list[Vote]:
    votes = await client_db.votes.find({"created_at": {"$gte": datetime.now() - timedelta(days=7)}}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_monthly_votes() -> list[Vote]:
    votes = await client_db.votes.find({"created_at": {"$gte": datetime.now() - timedelta(days=30)}}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_weekly_votes_by_poll_id(poll_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"poll_id": poll_id, "created_at": {"$gte": datetime.now() - timedelta(days=7)}}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]

async def get_monthly_votes_by_poll_id(poll_id: str) -> list[Vote]:
    votes = await client_db.votes.find({"poll_id": poll_id, "created_at": {"$gte": datetime.now() - timedelta(days=30)}}).to_list(length=1000)
    return [Vote(**vote) for vote in votes]