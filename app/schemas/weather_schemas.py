from typing import List
import strawberry
from datetime import datetime


@strawberry.type
class TimePointData:
    time_point: str
    humidity: int
    temperature: float


@strawberry.type
class WeatherData:
    city: str
    timePoints: List[TimePointData]
    createdAt: str = str(datetime.now())
    updatedAt: str = createdAt


@strawberry.type
class FavoriteLocationData:
    data: List[WeatherData]
