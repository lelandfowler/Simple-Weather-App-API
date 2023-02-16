from typing import Union, List
from app.schemas.input_schemas import WeatherDataInput, FavoriteForcastInput, AddFavoriteInput, DeleteFavoriteInput, \
    CreateUserInput
from app.schemas.utility_schemas import User, Message
from app.schemas.weather_schemas import FavoriteLocationData, WeatherData
from app.services.services import get_weather, validate_date
from pymongo import MongoClient
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import uvicorn

client = MongoClient("mongodb://localhost:27017/")
db = client["users_db"]
users_collection = db["users"]


async def get_user(
        user_id: str
) -> Union[User, Message]:
    user = users_collection.find_one({"userId": user_id})
    return User(userId=user_id, favorites=user["favorites"]) \
        if user else Message(message=f"NOT FOUND: User, {user_id}, was not found.")


async def get_users(
) -> List[User]:
    list_of_users = list(users_collection.find())
    return [User(userId=user["userId"], favorites=user["favorites"]) for user in list_of_users]


async def get_weather_data(
        input: WeatherDataInput
) -> Union[Message, WeatherData]:
    # Validate the Date Input
    error_message = validate_date(input.requestDate)
    if error_message:
        return error_message

    weather = get_weather(input.cityName, input.requestDate)
    return weather


async def get_favorite_forecast(
        input: FavoriteForcastInput
) -> Union[Message, FavoriteLocationData]:
    # Validate the Date Input
    error_message = validate_date(input.requestDate)
    if error_message:
        return error_message
    user = users_collection.find_one({"userId": input.userId})
    if 'favorites' in user:
        favorites = users_collection.find_one({"userId": input.userId})['favorites']
        weather = [get_weather(favorite, input.requestDate) for favorite in favorites]
        return FavoriteLocationData(data=weather)
    return Message(message=f"NO FORCAST: {input.userId}, does not have any favorites assigned.")


@strawberry.type
class Query:
    user: Union[User, Message] = strawberry.field(resolver=get_user)
    users: List[User] = strawberry.field(resolver=get_users)
    weather: Union[Message, WeatherData] = strawberry.field(resolver=get_weather_data)
    favoriteForecast: Union[Message, FavoriteLocationData] = strawberry.field(resolver=get_favorite_forecast)


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


@strawberry.type
class Mutation:
    createUser: Message = strawberry.mutation(resolver=createUser)
    addFavorite: Message = strawberry.mutation(resolver=add_favorite)
    deleteFavorite: Message = strawberry.mutation(resolver=delete_favorite)


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
