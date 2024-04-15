from fastapi import APIRouter, HTTPException, Depends
from models import Poll, User, Candidate, PollResults
from services import create_poll, update_poll, delete_poll, get_polls, get_results, get_general_results, update_status, publish_poll
from crud import get_current_active_user, get_polls_by_user_id, get_poll_by_id
from fastapi_utilities import repeat_at
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='update_status.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

router = APIRouter()

@router.post("/", response_model=None)
async def create_poll_endpoint(poll: Poll, user: User = Depends(get_current_active_user)):
    await create_poll(poll, user.id)

@router.get("/", response_model=list[Poll])
async def read_polls(user: User = Depends(get_current_active_user)):
    polls = await get_polls(user.id)
    return polls

@router.get("/me", response_model=list[Poll])
async def read_polls_me(user: User = Depends(get_current_active_user)):
    polls = await get_polls_by_user_id(user.id)
    return polls

@router.get("/{poll_id}/results", response_model=PollResults)
async def read_poll_results(poll_id: str, user: User = Depends(get_current_active_user)):
    return await get_results(poll_id, user)

@router.get("/results", response_model=PollResults)
async def read_all_poll_results(user: User = Depends(get_current_active_user)):
    return await get_general_results(user.polls, user.id)

@router.get("/{poll_id}", response_model=Poll)
async def read_poll(poll_id: str, user: User = Depends(get_current_active_user)):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.patch("/{poll_id}/publish", response_model=None)
async def publish_poll_endpoint(poll_id: str, user: User = Depends(get_current_active_user)):
    updated_poll = await publish_poll(poll_id, user)
    
    if updated_poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    return {"message": "Poll published"}

@router.patch("/{poll_id}", response_model=Poll)
async def update_poll_endpoint(poll_id: str, poll: Poll, user: User = Depends(get_current_active_user)):
    updated_poll = await update_poll(poll_id, poll)
    return updated_poll

@router.delete("/{poll_id}", response_model=None)
async def delete_poll_endpoint(poll_id: str, user: User = Depends(get_current_active_user)):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    await delete_poll(poll_id)

@router.on_event("startup")
@repeat_at(cron='0 7 * * *', logger=logger)
async def poll_results_scheduler():
    try:
        await update_status()
        logger.info("Poll status updated")
    except Exception as e:
        logger.error(f"Error updating poll status: {e}")