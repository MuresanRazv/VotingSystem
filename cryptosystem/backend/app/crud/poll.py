from database.connection import application_db
from models import Poll
from bson import ObjectId
from fastapi import HTTPException
from typing import Dict

async def create_poll(poll: Poll) -> str:
    poll_dict = poll.model_dump()
    inserted_poll = await application_db.polls.insert_one(poll_dict)
    return str(inserted_poll.inserted_id)

async def get_polls_by_user_id(user_id: str) -> list[Poll]:
    polls = await application_db.polls.find({"created_by": ObjectId(user_id)}, projection=None).to_list(length=1000)
    return [Poll(**poll) for poll in polls]

async def get_poll_by_id(poll_id: str) -> Poll:
    poll_dict = await application_db.polls.find_one({"_id": ObjectId(poll_id)})
    if (poll_dict is None):
        return None
    return Poll(**poll_dict)

async def get_polls(options: Dict) -> list[Poll]:
    polls = await application_db.polls.find(options, projection=None).to_list(length=1000)
    return [Poll(**poll) for poll in polls]

async def get_polls_by_status(status: str) -> list[Poll]:
    polls = await application_db.polls.find({"status": status}, projection=None).to_list(length=1000)
    return [Poll(**poll) for poll in polls]

async def delete_poll(poll_id: str):
    await application_db.polls.delete_one({"_id": ObjectId(poll_id)})

async def update_poll(poll_id: str, poll: Poll) -> Poll:
    poll_dict = poll.model_dump()
    updated_poll = await application_db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": poll_dict})
    if (updated_poll.modified_count == 0):
        raise HTTPException(status_code=404, detail="Poll not found")
    return await get_poll_by_id(poll_id)
