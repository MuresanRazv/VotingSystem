from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class Candidate(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

    name: str
    description: str