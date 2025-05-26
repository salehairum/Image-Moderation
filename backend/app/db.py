from motor.motor_asyncio import AsyncIOMotorClient #imports the asynchronous MongoDB client from the motor library
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

tokens_collection = db.tokens
usages_collection = db.usages