from database.connection import client_db
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models import TokenData
from jose import JWTError, jwt
from typing import Annotated
from models import User

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
    user_dict = await client_db.users.find_one({"_id": user_id})
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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def update_user(user_email: str, user: User) -> User:
    user_dict = user.model_dump(exclude_unset=True)
    await client_db.users.update_one({"email": user_email}, {"$set": user_dict})
    return await get_user_by_email(user.email)

async def delete_user(user_email: str):
    await client_db.users.delete_one({"email": user_email})