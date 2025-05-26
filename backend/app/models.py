from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    token: str
    isAdmin: bool = False
    createdAt: datetime
