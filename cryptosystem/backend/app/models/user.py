from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Dict

class User(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True
        
    username: str
    password: str
    email: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None
    # ObjectId => poll_id, str => decription key
    polls: Optional[Dict[ObjectId, str]] = None

class UpdatedUser(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    county: Optional[str] = None
    city: Optional[str] = None