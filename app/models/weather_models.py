from typing import Dict, List

import strawberry
from pydantic import BaseModel
from datetime import datetime


@strawberry.type
class TimePointData:
    time_point: str
    humidity: int
    temperature: float


@strawberry.type
class WeatherData:
    city: str
    time_points: List[TimePointData]
    creation_at: str = str(datetime.now())
    last_updated: str = creation_at


@strawberry.type
class FavoriteLocationData:
    data: List[WeatherData]
