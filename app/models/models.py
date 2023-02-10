from typing import Dict, List
from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    favorites: List[str] = []
    timestamp: str = str(datetime.now())


class TimePointData(BaseModel):
    time_point: str
    humidity: int
    temperature: float


class WeatherData(BaseModel):
    city: str
    time_points: List[TimePointData]
    timestamp: str = str(datetime.now())


class FavoriteLocationData(BaseModel):
    data: Dict[str, WeatherData] = {}
