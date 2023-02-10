import json
from math import floor
from typing import Dict
import requests
from decouple import config
from fastapi import HTTPException
from pydantic import BaseModel, validator
from datetime import date, timedelta


class DateModel(BaseModel):
    date: date

    @validator("date")
    def validate_date(cls, v):
        if v <= date.today() or v > date.today() + timedelta(days=3):
            raise HTTPException(
                status_code=400,
                detail=[
                    {
                        "loc": [
                            "query",
                            "request_date"
                        ],
                        "msg": "Date should be within the last year and today.",
                        "type": "value_error.date"
                    }
                ]
            )
        return v


def time_point_calculation(request_date: date):
    current_date = date.today()
    date_delta = request_date - current_date
    forcast_days = date_delta.days

    time_point_increment_hrs = 3
    time_points_per_day = floor(24 / time_point_increment_hrs)

    if forcast_days <= 0:
        raise ValueError("The request_date must be at least one day from the current_date.")
    total_count = forcast_days * time_points_per_day
    return total_count


def call_weather_api(city_name, total_count):
    units = "Imperial"
    API_KEY = config('API_KEY')

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": units,
        "cnt": total_count,
    }

    endpoint = f"http://api.openweathermap.org/data/2.5/forecast"

    request = requests.get(url=endpoint, params=params)

    if request.status_code != 200:
        # Pass exceptions in the weather api call through
        raise HTTPException(
            status_code=request.status_code,
            detail=[
                {
                    "msg": json.loads(request.text)["message"],
                }
            ]
        )
    return request.json()


def isolate_day_data(request_data, request_date):
    time_points_list = request_data["list"]
    day_data = [time_stamp for time_stamp in time_points_list if str(request_date) in time_stamp['dt_txt']]
    return day_data


def pull_weather_data(city_name: str, request_date: date):
    total_count = time_point_calculation(request_date)
    day_range_data = call_weather_api(city_name, total_count)
    single_day_data = isolate_day_data(day_range_data, request_date)
    return single_day_data


def clean_weather_data(json_data: Dict):
    output = {}
    for time_point_data in json_data:
        time_stamp = time_point_data['dt_txt']
        output[time_stamp] = {
            'temp': time_point_data['main']['temp'],
            'humidity': time_point_data['main']['humidity'],
        }
    return output
