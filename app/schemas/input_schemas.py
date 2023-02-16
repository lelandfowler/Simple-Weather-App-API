from datetime import date, timedelta
from typing import Optional
import strawberry


@strawberry.input
class WeatherDataInput:
    cityName: str
    requestDate: Optional[date] = date.today() + timedelta(days=1)


@strawberry.input
class FavoriteForcastInput:
    userId: str
    requestDate: date = date.today() + timedelta(days=1)


@strawberry.input
class AddFavoriteInput:
    userId: str
    newFavorite: str


@strawberry.input
class DeleteFavoriteInput:
    userId: str
    exFavorite: str
