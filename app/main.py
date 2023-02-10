from datetime import date, timedelta
from fastapi import FastAPI
from app.services import DateModel, clean_weather_data, pull_weather_data

import uvicorn

app = FastAPI()


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
            humidity: int
        }
    }
    """
    # Validate the Date Input
    DateModel.parse_obj({"date": request_date})

    data = pull_weather_data(city_name, request_date)
    result = clean_weather_data(data)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
