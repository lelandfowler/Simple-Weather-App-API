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

@strawberry.type
class Query:
    @strawberry.field
    def user(
            self,
            user_id: str
    ) -> Union[User, Message]:
        user = users_collection.find_one({"userId": user_id})
        return User(userId=user_id, favorites=user["favorites"]) \
            if user else Message(message=f"NOT FOUND: User, {user_id}, was not found.")

    @strawberry.field
    def users(
            self
    ) -> List[User]:
        list_of_users = list(users_collection.find())
        return [User(userId=user["userId"], favorites=user["favorites"]) for user in list_of_users]

    @strawberry.field
    def getWeatherData(
            self,
            input: WeatherDataInput
    ) -> Union[Message, WeatherData]:
        # Validate the Date Input
        error_message = validate_date(input.requestDate)
        if error_message:
            return error_message

        weather = get_weather(input.cityName, input.requestDate)
        return weather

    @strawberry.field
    def getFavoriteForcast(
            self,
            input: FavoriteForcastInput
    ) -> Union[Message, FavoriteLocationData]:
        # Validate the Date Input
        error_message = validate_date(input.requestDate)
        if error_message:
            return error_message

        favorites = users_collection.find_one({"userId": input.userId})['favorite']
        weather = [get_weather(favorite, input.requestDate) for favorite in favorites]
        return FavoriteLocationData(data=weather)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(
            self,
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

    @strawberry.mutation
    def addFavorite(
            self,
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

    @strawberry.mutation
    def deleteFavorite(
            self,
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


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
