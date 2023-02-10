import json
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


def pull_weather_data(city_name: str, request_date: date):
    current_date = date.today()
    date_delta = request_date - current_date
    forcast_days = date_delta.days
    units = "Imperial"
    API_KEY = config('API_KEY')

    endpoint = f"http://api.openweathermap.org/data/2.5/forecast?q=" \
               f"{city_name}&" \
               f"appid={API_KEY}&" \
               f"units={units}&" \
               f"cnt={forcast_days}"

    request = requests.get(url=endpoint)

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


def clean_weather_data(json_data: Dict):
    return json_data

