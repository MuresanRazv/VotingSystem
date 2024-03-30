from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict
from bson import ObjectId
from datetime import datetime

class Poll(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

    title: str
    description: str
    # ObjectId => candidate_id, str => encrypted count
    candidates: Optional[Dict[ObjectId, str]] = None
    encryption_key: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_by: Optional[ObjectId] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UpdatedPoll(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime