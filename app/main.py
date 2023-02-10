from typing import Dict
from decouple import config
from datetime import date, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import json
import requests
import uvicorn

app = FastAPI()


class Date_Model(BaseModel):
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


def clean_weather_data(json_data: Dict):
    return json_data


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{city_name}")
def get_weather_data(
        city_name: str,
        request_date: date = date.today() + timedelta(days=1)
):
    """
    :param city_name:
    :param request_date: Constrained to be within 1-3 days of the current date
    :return: a dictionary with datetime as the key and the value as a dictionary of parameters and values
    {
        date_time: {
            temperature: float
            humidity: int (0,100)
        }
    }
    """

    # Validate the Date Input
    Date_Model.parse_obj({"date": request_date})

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
    data = request.json()
    result = clean_weather_data(data)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
