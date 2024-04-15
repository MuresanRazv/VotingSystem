from pydantic import BaseModel, Field
from typing import Optional
from typing import List
from bson import ObjectId
from datetime import datetime
from models import Candidate

class Poll(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

    title: Optional[str] = None
    description: Optional[str] = None
    multiple_choice: Optional[bool] = False
    is_private: Optional[bool] = False
    is_revealed: Optional[bool] = False
    candidates: Optional[List[Candidate]]
    encryption_key: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_by: Optional[ObjectId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Optional[str] = None

class PollResults(BaseModel):
    poll_id: Optional[str] = None
    total_votes: int
    candidates: List[Candidate]
    county_statistics: dict
    votes_this_week: dict
    status: Optional[str] = None