from fastapi import APIRouter, HTTPException, Depends
from models import Poll, UpdatedPoll, User
from services import create_poll, create_poll_candidate
from crud import get_current_active_user, get_polls, get_polls_by_user_id, get_poll_by_id, remove_poll_candidate, update_poll_candidate, update_poll

router = APIRouter()

@router.post("/", response_model=None)
async def create_poll_endpoint(poll: UpdatedPoll, user: User = Depends(get_current_active_user)):
    print(user.id)
    await create_poll(poll, user.id)

@router.get("/", response_model=list[UpdatedPoll])
async def read_polls(user: str = Depends(get_current_active_user)):
    polls = await get_polls()
    return polls

@router.get("/me", response_model=list[UpdatedPoll])
async def read_polls_me(user: User = Depends(get_current_active_user)):
    polls = await get_polls_by_user_id(user.id)
    return polls

@router.get("/{poll_id}", response_model=UpdatedPoll)
async def read_poll(poll_id: str, user: str = Depends(get_current_active_user)):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.patch("/{poll_id}", response_model=UpdatedPoll)
async def update_poll_endpoint(poll_id: str, poll: UpdatedPoll, user: str = Depends(get_current_active_user)):
    updated_poll = await update_poll(poll_id, poll)
    return updated_poll

@router.post("/{poll_id}", response_model=UpdatedPoll)
async def add_candidate_endpoint(poll_id: str, poll: UpdatedPoll, user: str = Depends(get_current_active_user)):
    updated_poll = await create_poll_candidate(poll_id, poll)
    return updated_poll

@router.delete("/{poll_id}/candidate/{candidate_id}", response_model=UpdatedPoll)
async def remove_candidate_endpoint(poll_id: str, candidate_id: str, user: str = Depends(get_current_active_user)):
    updated_poll = await remove_poll_candidate(poll_id, candidate_id)
    return updated_poll

@router.put("/{poll_id}/candidate/{candidate_id}", response_model=UpdatedPoll)
async def update_candidate_endpoint(poll_id: str, candidate_id: str, poll: UpdatedPoll, user: str = Depends(get_current_active_user)):
    updated_poll = await update_poll_candidate(poll_id, candidate_id, poll)
    return updated_poll
