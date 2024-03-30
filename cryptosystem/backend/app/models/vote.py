from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Dict, Optional

class Vote(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
    
    title: str
    description: str
    candidates: Optional[Dict[ObjectId, str]]
    poll_id: ObjectId
    user_id: ObjectId