from typing import Union, List
from app.db.db_management import users_collection
from app.schemas.input_schemas import CreateUserInput, AddFavoriteInput, DeleteFavoriteInput
from app.schemas.utility_schemas import Message, User


async def get_user(
        user_id: str
) -> Union[User, Message]:
    user = users_collection.find_one({"userId": user_id})
    return User(userId=user_id, favorites=user["favorites"]) \
        if user else Message(message=f"NOT FOUND: User, {user_id}, was not found.")


async def get_users() -> List[User]:
    list_of_users = list(users_collection.find())
    return [User(userId=user["userId"], favorites=user["favorites"]) for user in list_of_users]


async def createUser(
        input: CreateUserInput
) -> Message:
    if users_collection.find_one({"userId": input.userId}):
        return Message(message=f"NOT CREATED: User, {input.userId}, already exists.")

    if input.favorites is None:
        favorites = []
    else:
        favorites = input.favorites

    users_collection.insert_one({"userId": input.userId, "favorites": favorites})
    return Message(message=f"CREATED: User, {input.userId}, created.")


async def add_favorite(
        input: AddFavoriteInput
) -> Message:
    user = users_collection.find_one({"userId": input.userId})
    favorites = user['favorites']
    if user is None:
        return Message(message=f"NOT UPDATED: User, {input.userId}, was not found.")
    if input.newFavorite not in favorites:
        favorites.append(input.newFavorite)
        users_collection.update_one(
            {"userId": input.userId},
            {"$set": {"favorites": favorites}}
        )
        return Message(message=f"UPDATED: {input.newFavorite}, has been added to {input.userId}'s "
                               f"list of favorites: {favorites}")
    return Message(message=f"NOT UPDATED: {input.newFavorite}, is already on {input.userId}'s "
                           f"list of favorites: {favorites}")


async def delete_favorite(
        input: DeleteFavoriteInput
) -> Message:
    user = users_collection.find_one({"userId": input.userId})
    favorites = user['favorites']
    if user is None:
        return Message(message=f"User, {input.userId}, does not exists.")
    if input.exFavorite in favorites:
        favorites.remove(input.exFavorite)
        users_collection.update_one(
            {"userId": input.userId},
            {"$set": {"favorites": favorites}}
        )
        return Message(message=f"Success: {input.exFavorite}, has been removed from {input.userId}'s "
                               f"list of favorites: {favorites}")
    return Message(message=f"That location is not on the User's, {input.userId}, favorites list.")
