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
    candidates: Dict[ObjectId, str]
    encryption_key: str
    start_date: datetime
    end_date: datetime
    created_by: ObjectId
    created_at: datetime
    updated_at: datetime

class UpdatedPoll(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
    
    title: str
    description: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]