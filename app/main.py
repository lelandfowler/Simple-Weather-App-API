from datetime import datetime, date, timedelta

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{city_name}")
def get_weather_data(city_name: str, response_date: date):
    return {f"{city_name}: {response_date}"}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)
