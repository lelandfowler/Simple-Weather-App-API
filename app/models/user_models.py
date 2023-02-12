from typing import List

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    favorites: List[str] = []
    timestamp: str = str(datetime.now())

