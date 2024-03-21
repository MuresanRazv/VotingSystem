from fastapi import APIRouter, HTTPException
from models import Candidate
from crud import create_candidate, get_candidate, update_candidate, delete_candidate

router = APIRouter()

@router.post("/", response_model=Candidate)
async def create_candidate_endpoint(candidate: Candidate):
    created_candidate = await create_candidate(candidate)
    return created_candidate

@router.get("/{candidate_id}", response_model=Candidate)
async def get_candidate_endpoint(candidate_id: str):
    db_candidate = await get_candidate(candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.put("/{candidate_id}", response_model=Candidate)
async def update_candidate_endpoint(candidate_id: str, candidate: Candidate):
    db_candidate = await get_candidate(candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    updated_candidate = await update_candidate(candidate_id, candidate)
    return updated_candidate

@router.delete("/{candidate_id}")
async def delete_candidate_endpoint(candidate_id: str):
    db_candidate = await delete_candidate(candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "User deleted successfully"}