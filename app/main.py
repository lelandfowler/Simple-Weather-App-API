from typing import Union, List
from app.resolvers.user_resolvers \
    import get_users, get_user, createUser, add_favorite, delete_favorite
from app.resolvers.weather_resolvers import get_weather_data, get_favorite_forecast
from app.schemas.utility_schemas import User, Message
from app.schemas.weather_schemas import FavoriteLocationData, WeatherData
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry
import uvicorn


@strawberry.type
class Query:
    user: Union[User, Message] = strawberry.field(resolver=get_user)
    users: List[User] = strawberry.field(resolver=get_users)
    weather: Union[Message, WeatherData] = strawberry.field(resolver=get_weather_data)
    favoriteForecast: Union[Message, FavoriteLocationData] = strawberry.field(resolver=get_favorite_forecast)


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
