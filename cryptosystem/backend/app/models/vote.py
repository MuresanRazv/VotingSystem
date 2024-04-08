from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
from models import Candidate, Poll
from datetime import datetime

class Vote(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

    candidates: Optional[List[Candidate]]
    poll_id: str
    user_id: str
    created_at: Optional[datetime] = None

class ResponseVote(BaseModel):
    poll: Optional[Poll]