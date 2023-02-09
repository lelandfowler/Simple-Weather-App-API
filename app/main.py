import json
from typing import Dict
from decouple import config
from datetime import datetime, date, timedelta
import requests
import uvicorn
from fastapi import FastAPI, Query, Path, HTTPException

app = FastAPI()


def clean_weather_data(json_data: Dict):
    return json_data


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{city_name}")
def get_weather_data(
        city_name: str,
        request_date: date = Query(
            None,
            description="The date that user would like to see data for.",
        )
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
        raise HTTPException(status_code=request.status_code, detail=json.loads(request.text))
    data = request.json()
    result = clean_weather_data(data)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
