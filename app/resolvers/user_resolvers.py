from typing import Union
from app.main import users_collection
from app.schemas.utility_schemas import Message, User


async def get_user(
            user_id: str
    ) -> Union[User, Message]:
        user = users_collection.find_one({"userId": user_id})
        return User(userId=user_id, favorites=user["favorites"]) \
            if user else Message(message=f"NOT FOUND: User, {user_id}, was not found.")