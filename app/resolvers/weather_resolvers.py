from typing import Union
from app.db.db_management import users_collection
from app.schemas.input_schemas import WeatherDataInput, FavoriteForcastInput
from app.schemas.utility_schemas import Message
from app.schemas.weather_schemas import WeatherData, FavoriteLocationData
from app.services.services import validate_date, get_weather


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

