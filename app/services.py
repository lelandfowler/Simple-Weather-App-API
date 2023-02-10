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
    initial_offset = 1  # The weather API excludes the 0 hour time-point for the first day
    array_offset = 1


    if forcast_days <= 0:
        raise ValueError("The request_date must be at least one day from the current_date.")

    last_time_point_index = forcast_days * time_points_per_day - initial_offset - array_offset
    if forcast_days > 1:
        first_time_point_index = last_time_point_index - time_points_per_day
    else:
        first_time_point_index = 0

    return first_time_point_index, last_time_point_index


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


def isolate_day_data(day_range_data, first_time_point_index, last_time_point_index):
    time_points = day_range_data["list"]
    return time_points[first_time_point_index:last_time_point_index]


def pull_weather_data(city_name: str, request_date: date):
    first_time_point_index, last_time_point_index \
        = time_point_calculation(request_date)
    day_range_data = call_weather_api(city_name, last_time_point_index)
    single_day_data = isolate_day_data(day_range_data, first_time_point_index, last_time_point_index)
    return single_day_data


def clean_weather_data(json_data: Dict):
    return json_data
