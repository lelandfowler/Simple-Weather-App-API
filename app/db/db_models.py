from typing import List
from pydantic import BaseModel


class DbUser(BaseModel):
    userId: str
    favorites: List[str]

