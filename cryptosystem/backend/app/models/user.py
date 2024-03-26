from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

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
    full_name: Optional[str] = None
    address: Optional[str] = None
    disabled: Optional[bool] = None

class UpdatedUser(BaseModel):
    full_name: Optional[str] = None
    address: Optional[str] = None