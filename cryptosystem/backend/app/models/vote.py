from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
from models import Candidate

class Vote(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
    
    title: str
    description: str
    candidates: Optional[List[Candidate]]
    poll_id: ObjectId
    user_id: ObjectId