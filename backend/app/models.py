from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    token: str
    isAdmin: bool = False
    createdAt: datetime

#this model is for creating a new token as date is not passed
class TokenRequest(BaseModel):
    token: str 
    isAdmin: bool = False