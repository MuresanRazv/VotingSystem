from database.connection import client_db
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models import TokenData
from jose import JWTError, jwt
from typing import Annotated
from models import User, UpdatedUser
from bson import ObjectId
import os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

async def create_user(user: User) -> User:
    user_dict = user.model_dump()

    # check if user with email already exists
    if await get_user_by_email(user.email) is not None:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    inserted_user = await client_db.users.insert_one(user_dict)
    user._id = inserted_user.inserted_id
    return user

async def get_user_by_id(user_id: str) -> User:
    user_dict = await client_db.users.find_one({"_id": ObjectId(user_id)})
    if (user_dict is None):
        return None
    return User(**user_dict)

async def get_user_by_email(user_mail: str) -> User:
    user_dict = await client_db.users.find_one({"email": user_mail})
    if (user_dict is None):
        return None
    return User(**user_dict)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_id(token_data.id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

async def update_user(user_id: str, user: UpdatedUser) -> User:
    user_dict = user.model_dump(exclude_unset=True)

    try:
        result = await client_db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"No user found with ID {user_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HTTP error occurred while updating user document: {e}")
    
    return await get_user_by_id(user_id)

async def delete_user(user_id: str):
    await client_db.users.delete_one({"_id": ObjectId(user_id)})