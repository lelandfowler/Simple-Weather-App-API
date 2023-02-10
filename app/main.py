from datetime import date, timedelta, datetime
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
from app.services import DateModel, clean_weather_data, pull_weather_data
import uvicorn

app = FastAPI()

users = {

}


class User(BaseModel):
    favorites: List[str] = []
    created: str = str(datetime.now())


class TimePointData(BaseModel):
    timestamp: str
    humidity: int
    temperature: float


class WeatherData(BaseModel):
    city: str
    time_stamps: List[TimePointData]


class FavoriteLocationData(BaseModel):
    data: List[WeatherData]


users['user_1'] = User()
users['user_2'] = User()
users['user_3'] = User()


@app.get("/user")
async def create_user(uid: str):
    matching_list = [user for user in users if uid == user]
    if len(matching_list) == 1:
        user = users[uid]
        return {"message": {uid: user}}
    else:
        return {"message": f"User, {uid}, does not exist."}


@app.post("/user")
async def create_user(uid: str):
    matching_list = [user for user in users if uid == user]
    if len(matching_list) == 1:
        return {"message": f"User, {uid}, already exists."}
    else:
        user = User()
        users[uid] = user
        return {"message": f"Success: User, {uid}, created."}


@app.post("/favorite")
async def update_favorite(uid: str, favorite: str):
    matching_list = [user for user in users if uid == user]
    if len(matching_list) == 0:
        return {"message": f"User, {uid}, does not exists."}

    favorites = users[uid] .favorites
    if favorite not in favorites:
        favorites.append(favorite)
        return {"message": f"Success: {favorite}, has been added to {uid}'s list of favorites: {favorites}"}

    return {"message": f"That location is already on User's, {uid}, favorites list."}

@app.delete("/favorite")
async def add_favorite(uid: str, favorite: str):
    matching_list = [user for user in users if uid == user]
    if len(matching_list) == 0:
        return {"message": f"User, {uid}, does not exists."}

    favorites = users[uid] .favorites
    if favorite not in favorites:
        favorites.append(favorite)
        return {"message": f"Success: {favorite}, has been added to {uid}'s list of favorites: {favorites}"}

    return {"message": f"That location is already on User's, {uid}, favorites list."}


@app.get("/favorite_forecast")
async def get_favorite_forcast():
    pass


@app.get("/weather_forecast")
async def get_weather_data(
        city_name: str,
        request_date: date = date.today() + timedelta(days=1)
):
    """
    :param city_name: name of city to query from the open weather api, not case-sensitive,
    must match exact spelling of city name in english
    :param request_date: Constrained to be within 1-3 days of the current date
    :return: a dictionary with datetime as the key and the value as a dictionary
    of parameters and values
    {
        date_time: {
            temperature: float
            humidity: int
        }
    }
    """
    # Validate the Date Input
    DateModel.parse_obj({"date": request_date})

    raw_weather_data = pull_weather_data(city_name, request_date)
    clean_weather = clean_weather_data(raw_weather_data)
    return clean_weather


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
