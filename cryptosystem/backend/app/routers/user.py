from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models import User, UpdatedUser
from crud import create_user, get_user_by_id, get_user_by_email, update_user, delete_user, get_current_active_user
import bcrypt
from urllib.parse import unquote

router = APIRouter()

@router.post("/", response_model=User)
async def create_user_endpoint(user: User):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')

    created_user = await create_user(user)
    return created_user

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.patch("/{user_id}", response_model=User)
async def update_user_endpoint(user_id: str, user: UpdatedUser):
    db_user = await get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await update_user(user_id, user)
    return updated_user

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    db_user = await get_user_by_id(unquote(user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(unquote(user_id))
    return {"message": "User deleted successfully"}