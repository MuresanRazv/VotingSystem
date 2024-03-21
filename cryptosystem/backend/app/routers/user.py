from fastapi import APIRouter, HTTPException
from models import User
from crud import create_user, get_user_by_id, get_user_by_email, update_user, delete_user
import bcrypt

router = APIRouter()

@router.post("/", response_model=User)
async def create_user_endpoint(user: User):
    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password.decode('utf-8')

    created_user = await create_user(user)
    return created_user

@router.get("/{user_id}", response_model=User)
async def get_user_by_id_endpoint(user_id: str):
    db_user = await get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_mail}",  response_model=User)
async def get_user_by_email_endpoint(user_mail: str):
    db_user = await get_user_by_email(user_mail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=User)
async def update_user_endpoint(user_id: str, user: User):
    db_user = await get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await update_user(user_id, user)
    return updated_user

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: str):
    db_user = await get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(user_id)
    return {"message": "User deleted successfully"}