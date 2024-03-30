from database.connection import application_db
from models import Poll, UpdatedPoll
from bson import ObjectId
from fastapi import HTTPException

async def create_poll(poll: Poll) -> str:
    poll_dict = poll.model_dump()
    inserted_poll = await application_db.polls.insert_one(poll_dict)
    return str(inserted_poll.inserted_id)

async def get_polls_by_user_id(user_id: str) -> list[Poll]:
    polls = await application_db.polls.find({"created_by": ObjectId(user_id)}).to_list(length=1000)
    return [Poll(**poll) for poll in polls]

async def get_poll_by_id(poll_id: str) -> Poll:
    poll_dict = await application_db.polls.find_one({"_id": ObjectId(poll_id)})
    if (poll_dict is None):
        return None
    return Poll(**poll_dict)

async def get_polls() -> list[Poll]:
    polls = await application_db.polls.find().to_list(length=1000)
    return [Poll(**poll) for poll in polls]

async def delete_poll(poll_id: str):
    await application_db.polls.delete_one({"_id": ObjectId(poll_id)})

async def update_poll(poll_id: str, poll: Poll) -> Poll:
    poll_dict = poll.model_dump()

    try:
        result = await application_db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": poll_dict})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Poll not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error updating poll")

    return await get_poll_by_id(poll_id)

async def create_poll_candidate(poll_id: str, candidate_id: str, encrypted_count: str):
    await application_db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": {"candidates." + candidate_id: encrypted_count}})

async def remove_poll_candidate(poll_id: str, candidate_id: str):
    await application_db.polls.update_one({"_id": ObjectId(poll_id)}, {"$unset": {"candidates." + candidate_id: ""}})

async def update_poll_candidate(poll_id: str, candidate_id: str, poll: UpdatedPoll):
    poll_dict = poll.model_dump()
    await application_db.polls.update_one({"_id": ObjectId(poll_id)}, {"$set": {"candidates." + candidate_id: poll_dict["candidates"][candidate_id]}})
    return await get_poll_by_id(poll_id)