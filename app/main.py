from decouple import config
from datetime import datetime, date, timedelta
import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{city_name}")
def get_weather_data(city_name: str, request_date: date):
    # Take the city name and date and return the forcast for that day
    # If the date is > 3 days then return an error from the current date then
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
    j_request = request.json()
    status_code = request.status_code
    return {f"status code: {status_code}": j_request}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
