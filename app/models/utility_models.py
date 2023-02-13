from typing import List, Optional
import strawberry
from datetime import datetime


@strawberry.type
class User:
    user_id: str
    favorites: Optional[List[str]]
    creation_at: str = str(datetime.now())
    last_updated: str = creation_at


@strawberry.type
class Message:
    message: str
