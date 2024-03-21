from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    _id: Optional[ObjectId] = None
    username: str
    password: str
    email: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    CNP: Optional[str] = None