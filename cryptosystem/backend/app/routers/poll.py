from fastapi import APIRouter, HTTPException, Depends
from models import Poll, User, Candidate, PollResults
from services import create_poll, update_poll, delete_poll, get_polls, get_results, get_general_results
from crud import get_current_active_user, get_polls_by_user_id, get_poll_by_id
from typing import List

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
    return await get_results(poll_id, user.polls)

@router.get("/results", response_model=PollResults)
async def read_all_poll_results(user: User = Depends(get_current_active_user)):
    return await get_general_results(user.polls)

@router.get("/{poll_id}", response_model=Poll)
async def read_poll(poll_id: str, user: User = Depends(get_current_active_user)):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

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