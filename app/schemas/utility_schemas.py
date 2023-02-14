from typing import List, Optional
import strawberry
from datetime import datetime


@strawberry.type
class User:
    userId: str
    favorites: Optional[List[str]]
    createdAt: str = str(datetime.now())
    updatedAt: str = createdAt


@strawberry.type
class Message:
    message: str
