from database.connection import client_db
from models import User

async def create_user(user: User) -> User:
    user_dict = user.model_dump()
    inserted_user = await client_db.users.insert_one(user_dict)
    user._id = inserted_user.inserted_id
    return user

async def get_user_by_id(user_id: str) -> User:
    user_dict = await client_db.users.find_one({"_id": user_id})
    return User(**user_dict)

async def get_user_by_email(user_mail: str) -> User:
    user_dict = await client_db.users.find_one({"email": user_mail})
    return User(**user_dict)

async def update_user(user_id: str, user: User) -> User:
    user_dict = user.model_dump(exclude_unset=True)
    await client_db.users.update_one({"_id": user_id}, {"$set": user_dict})
    return user

async def delete_user(user_id: str):
    await client_db.users.delete_one({"_id": user_id})