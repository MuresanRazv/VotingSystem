from database.connection import client_db
from models import Candidate
from typing import List

async def create_candidate(candidate: Candidate) -> Candidate:
    candidate_dict = candidate.model_dump()
    inserted_candidate = await client_db.candidates.insert_one(candidate_dict)
    candidate._id = inserted_candidate._id
    return candidate

async def create_candidates(candidates: List[Candidate]) -> List[Candidate]:
    inserted_candidates = []
    for candidate in candidates:
        inserted_candidates.append(create_candidate(candidate))

    return inserted_candidates

async def get_candidate(candidate_id: str) -> Candidate:
    candidate_dict = await client_db.candidates.find_one({"_id": candidate_id})
    return Candidate(**candidate_dict)

async def update_candidate(candidate_id: str, candidate: Candidate) -> Candidate:
    candidate_dict = candidate.model_dump(exclude_unset=True)
    await client_db.users.update_one({"_id": candidate_id}, {"$set": candidate_dict})
    return candidate

async def delete_candidate(candidate_id: str):
    await client_db.candidates.delete_one({"_id": candidate_id})