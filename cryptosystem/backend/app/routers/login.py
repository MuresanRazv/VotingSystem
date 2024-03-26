from fastapi import APIRouter, HTTPException
from models import User, Login, Token
from crud import get_user_by_email
from jose import JWTError, jwt
from fastapi import Depends
from fastapi import status
import bcrypt
from datetime import datetime, timedelta, timezone

router = APIRouter()

SECRET_KEY = "d46d1f1fcc364a513277fda8e503ae4de3c81c30474b59165cd46dc717e04ef2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/", response_model=Token)
async def login(user: Login):
    db_user = await get_user_by_email(user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")