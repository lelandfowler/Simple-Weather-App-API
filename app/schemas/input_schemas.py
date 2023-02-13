from datetime import date, timedelta
from typing import Optional
import strawberry


@strawberry.input
class WeatherDataInput:
    city_name: str
    request_date: Optional[date] = date.today() + timedelta(days=1)
