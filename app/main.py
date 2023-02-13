from typing import Union, List
from app.config.user_config import user_dict
from app.schemas.input_schemas import WeatherDataInput, FavoriteForcastInput, AddFavoriteInput, DeleteFavoriteInput
from app.schemas.utility_schemas import User, Message
from app.schemas.weather_schemas import FavoriteLocationData, WeatherData
from app.services.services import get_weather, validate_date
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import uvicorn


@strawberry.type
class Query:
    @strawberry.field
    def user(
            self,
            userId: str
    ) -> Union[User, Message]:
        favorites = user_dict.get(userId)
        return User(userId=userId, favorites=favorites) \
            if userId in user_dict else Message(message=f"NOT FOUND: User, {userId}, was not found.")

    @strawberry.field
    def users(
            self
    ) -> List[User]:
        return [User(userId=uid, favorites=favorites) for uid, favorites in user_dict.items()]

    @strawberry.field
    def getWeatherData(
            self,
            input: WeatherDataInput
    ) -> Union[Message, WeatherData]:
        # Validate the Date Input
        error_message = validate_date(input.request_date)
        if error_message:
            return error_message

        weather = get_weather(input.city_name, input.request_date)
        return weather

    @strawberry.field
    def getFavoriteForcast(
            self,
            input: FavoriteForcastInput
    ) -> Union[Message, FavoriteLocationData]:
        # Validate the Date Input
        error_message = validate_date(input.request_date)
        if error_message:
            return error_message

        favorites = user_dict.get(input.userId)
        weather = [get_weather(favorite, input.request_date) for favorite in favorites]
        return FavoriteLocationData(data=weather)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(
            self,
            userId: str
    ) -> Message:
        if userId in user_dict:
            return Message(message=f"NOT CREATED: User, {userId}, already exists.")
        user_dict[userId] = []
        return Message(message=f"CREATED: User, {userId}, created.")

    @strawberry.mutation
    def addFavorite(
            self,
            input: AddFavoriteInput
    ) -> Message:
        favorites = user_dict.get(input.userId)
        if favorites is None:
            return Message(message=f"NOT UPDATED: User, {input.userId}, was not found.")
        if input.newFavorite not in user_dict[input.userId]:
            user_dict[input.userId].append(input.newFavorite)
            return Message(message=f"UPDATED: {input.newFavorite}, has been added to {input.userId}'s "
                                   f"list of favorites: {favorites}")
        return Message(message=f"NOT UPDATED: {input.newFavorite}, is already on {input.userId}'s "
                               f"list of favorites: {favorites}")

    @strawberry.mutation
    def deleteFavorite(
            self,
            input: DeleteFavoriteInput
    ) -> Message:
        favorites = user_dict.get(input.userId)
        if favorites is None:
            return Message(message=f"User, {input.userId}, does not exists.")
        if input.exFavorite in favorites:
            favorites.remove(input.exFavorite)
            return Message(message=f"Success: {input.exFavorite}, has been removed from {input.userId}'s "
                                   f"list of favorites: {favorites}")
        return Message(message=f"That location is not on the User's, {input.userId}, favorites list.")


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
