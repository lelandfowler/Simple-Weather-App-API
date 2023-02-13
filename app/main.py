from datetime import date, timedelta
from typing import Union, List, Optional
from app.config.user_config import user_dict
from app.models.utility_models import User
from app.models.utility_models import Message
from app.models.weather_models import FavoriteLocationData, WeatherData
from app.services.services import get_weather, validate_date
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn


# @app.get("/user")
# async def create_user(uid: str):
#     matching_list = [user for user in users if uid == user]
#     if len(matching_list) == 1:
#         user = users[uid]
#         return {"message": {uid: user}}
#     else:
#         return {"message": f"User, {uid}, does not exist."}
#
#
# @app.post("/user")
# async def create_user(uid: str):
#     matching_list = [user for user in users if uid == user]
#     if len(matching_list) == 1:
#         return {"message": f"User, {uid}, already exists."}
#     else:
#         user = User()
#         users[uid] = user
#         return {"message": f"Success: User, {uid}, created."}
#
#
# @app.post("/favorite")
# async def update_favorite(uid: str, favorite: str):
#     matching_list = [user for user in users if uid == user]
#     if len(matching_list) == 0:
#         return {"message": f"User, {uid}, does not exists."}
#
#     favorites = users[uid].favorites
#     if favorite not in favorites:
#         favorites.append(favorite)
#         return {"message": f"Success: {favorite}, has been added to {uid}'s list of favorites: {favorites}"}
#
#     return {"message": f"That location is already on User's, {uid}, favorites list."}
#
#
# @app.delete("/favorite")
# async def delete_favorite(uid: str, favorite: str):
#     matching_list = [user for user in users if uid == user]
#     if len(matching_list) == 0:
#         return {"message": f"User, {uid}, does not exists."}
#
#     favorites = users[uid].favorites
#     if favorite in favorites:
#         favorites.remove(favorite)
#         return {"message": f"Success: {favorite}, has been removed from {uid}'s list of favorites: {favorites}"}
#
#     return {"message": f"That location is not on the User's, {uid}, favorites list."}
#
#
# @app.get("/favorite_forecast")
# async def get_favorite_forcast(
#         uid: str,
#         request_date: date = date.today() + timedelta(days=1)
# ):
#     # Validate the Date Input
#     DateModel.parse_obj({"date": request_date})
#
#     favorite_forcast = FavoriteLocationData()
#
#     favorites = users[uid].favorites
#     for favorite in favorites:
#         weather = get_weather(favorite, request_date)
#         favorite_forcast.data[favorite] = weather
#     return {"message": favorite_forcast}
#
#
# @app.get("/weather_forecast")
# async def get_weather_data(
#         city_name: str,
#         request_date: date = date.today() + timedelta(days=1)
# ):
#     """
#     :param city_name: name of city to query from the open weather api, not case-sensitive,
#     must match exact spelling of city name in english
#     :param request_date: Constrained to be within 1-3 days of the current date
#     :return: a list of TimePointData
#     """
#     # Validate the Date Input
#     DateModel.parse_obj({"date": request_date})
#
#     weather = get_weather(city_name, request_date)
#     return weather


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
    def get_weather_data(
            self,
            city_name: str,
            request_date: Optional[date] = date.today() + timedelta(days=1)
    ) -> Union[Message, WeatherData]:
        """
        :param city_name: name of city to query from the open weather api, not case-sensitive,
        must match exact spelling of city name in english
        :param request_date: constrained to be within 1-3 days of the current date
        :return: WeatherData object
        """
        # Validate the Date Input
        error_message = validate_date(request_date)
        if error_message:
            return error_message

        weather = get_weather(city_name, request_date)
        return weather


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, user_id: str) -> Message:
        if user_id in user_dict:
            return Message(message=f"NOT CREATED: User, {user_id}, already exists.")
        user_dict[user_id] = []
        return Message(message=f"CREATED: User, {user_id}, created.")


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
