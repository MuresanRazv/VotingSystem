from models import User, Vote
from crud import get_current_active_user, get_poll_by_id, get_votes_by_poll_id
from services import add_vote, create_vote
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