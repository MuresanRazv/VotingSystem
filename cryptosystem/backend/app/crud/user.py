from database.connection import client_db
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models import TokenData
from jose import JWTError, jwt
from typing import Annotated
from models import User, UpdatedUser
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "d46d1f1fcc364a513277fda8e503ae4de3c81c30474b59165cd46dc717e04ef2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def create_user(user: User) -> User:
    user_dict = user.model_dump()
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
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def update_user(user_id: str, user: UpdatedUser) -> User:
    user_dict = user.model_dump(exclude_unset=True)

    try:
        result = await client_db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
        if result.matched_count == 0:
            raise HTTPException(status=404, text=f"No user found with ID {user_id}")
    except Exception as e:
        raise HTTPException(status=500, text=f"HTTP error occurred while updating user document: {e}")
    
    return await get_user_by_id(user_id)

async def delete_user(user_id: str):
    await client_db.users.delete_one({"_id": ObjectId(user_id)})