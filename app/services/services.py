import json
from math import floor
from typing import List
import requests
from decouple import config
from fastapi import HTTPException
from datetime import date, timedelta
from app.models.utility_models import Message
from app.models.weather_models import TimePointData, WeatherData


def validate_date(input_date):
    if input_date < date.today() + timedelta(days=1) or input_date > date.today() + timedelta(days=3):
        return Message(message=f"Date should be within 1-3 days of the current date({date.today()}).")
    return None


def time_point_calculation(request_date: date):
    current_date = date.today()
    date_delta = request_date - current_date
    forcast_days = date_delta.days + 1

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
    day_data = []
    for time_point in time_points_list:
        tp_in_data = time_point['dt_txt']
        if str(request_date) in tp_in_data:
            day_data.append(time_point)
    # day_data = [time_point for time_point in time_points_list if str(request_date) in time_point['dt_txt']]
    return day_data


def pull_raw_weather_data(city_name: str, request_date: date):
    total_count = time_point_calculation(request_date)
    day_range_data = call_weather_api(city_name, total_count)
    single_day_data = isolate_day_data(day_range_data, request_date)
    return single_day_data


def clean_weather_data(json_data: List):
    time_points = []
    for time_point_data in json_data:
        time_point = time_point_data['dt_txt']
        time_points.append(
            TimePointData(
                time_point=time_point,
                humidity=time_point_data['main']['humidity'],
                temperature=time_point_data['main']['temp']
            )
        )
    return time_points


def get_weather(city_name, request_date):
    raw_weather_data = pull_raw_weather_data(city_name, request_date)
    time_points = clean_weather_data(raw_weather_data)
    return WeatherData(city=city_name, time_points=time_points)
