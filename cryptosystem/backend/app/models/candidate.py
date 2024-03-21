from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Candidate(BaseModel):
    _id: Optional[ObjectId] = None
    name: str
    description: str