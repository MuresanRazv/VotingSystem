from app.models import User, Vote, ResponseVote
from app.crud import get_current_active_user, get_poll_by_id, get_votes_by_poll_id
from app.services import add_vote, create_vote, get_votes_by_user_id
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.post("/{poll_id}/vote")
async def vote(poll_id: str, vote: Vote, user: User = Depends(get_current_active_user)):
    poll = await get_poll_by_id(poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found")
    
    vote = await create_vote(user.id, poll_id, vote)
    return await add_vote(poll_id, vote, user.id)

@router.get("/{poll_id}/votes", response_model=list[Vote])
async def read_votes(poll_id: str, user: User = Depends(get_current_active_user)):
    votes = await get_votes_by_poll_id(poll_id)
    return votes

@router.get("/{user_id}", response_model=list[ResponseVote])
async def read_votes_by_user(user_id: str, user: User = Depends(get_current_active_user)):
    votes = await get_votes_by_user_id(user_id)
    return votes