from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import user as user_model
from app.crud import user as user_crud
import bcrypt
from urllib.parse import unquote

router = APIRouter()

@router.post("/", response_model=user_model.User)
async def create_user_endpoint(user: user_model.User):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')

    created_user = await user_crud.create_user(user)
    return created_user

@router.get("/me", response_model=user_model.User)
async def read_users_me(current_user: user_model.User = Depends(user_crud.get_current_active_user)):
    return current_user

@router.patch("/{user_id}", response_model=user_model.User)
async def update_user_endpoint(user_id: str, user: user_model.UpdatedUser):
    db_user = await user_crud.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await user_crud.update_user(user_id, user)
    return updated_user

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    db_user = await user_crud.get_user_by_id(unquote(user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user_crud.delete_user(unquote(user_id))
    return {"message": "User deleted successfully"}