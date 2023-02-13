from datetime import date, timedelta
from typing import Union, List, Optional
from app.config.user_config import user_dict
from app.schemas.input_schemas import WeatherDataInput
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
    def user(self, user_id: str) -> Union[User, Message]:
        favorites = user_dict.get(user_id)
        return User(user_id=user_id, favorites=favorites) \
            if user_id in user_dict else Message(message=f"NOT FOUND: User, {user_id}, was not found.")

    @strawberry.field
    def users(self) -> List[User]:
        return [User(user_id=uid, favorites=favorites) for uid, favorites in user_dict.items()]

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
            user_id: str,
            request_date: date = date.today() + timedelta(days=1)
    ) -> Union[Message, FavoriteLocationData]:
        # Validate the Date Input
        error_message = validate_date(request_date)
        if error_message:
            return error_message

        favorites = user_dict.get(user_id)
        weather = [get_weather(favorite, request_date) for favorite in favorites]
        return FavoriteLocationData(data=weather)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, user_id: str) -> Message:
        if user_id in user_dict:
            return Message(message=f"NOT CREATED: User, {user_id}, already exists.")
        user_dict[user_id] = []
        return Message(message=f"CREATED: User, {user_id}, created.")

    @strawberry.mutation
    def addFavorite(self, user_id: str, new_favorite: str) -> Message:
        favorites = user_dict.get(user_id)
        if favorites is None:
            return Message(message=f"NOT UPDATED: User, {user_id}, was not found.")
        if new_favorite not in user_dict[user_id]:
            user_dict[user_id].append(new_favorite)
            return Message(message=f"UPDATED: {new_favorite}, has been added to {user_id}'s "
                                   f"list of favorites: {favorites}")
        return Message(message=f"NOT UPDATED: {new_favorite}, is already on {user_id}'s "
                               f"list of favorites: {favorites}")

    @strawberry.mutation
    def deleteFavorite(self, user_id: str, favorite: str) -> Message:
        favorites = user_dict.get(user_id)
        if favorites is None:
            return Message(message=f"User, {user_id}, does not exists.")
        if favorite in favorites:
            favorites.remove(favorite)
            return Message(message=f"Success: {favorite}, has been removed from {user_id}'s "
                                   f"list of favorites: {favorites}")
        return Message(message=f"That location is not on the User's, {user_id}, favorites list.")


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)
