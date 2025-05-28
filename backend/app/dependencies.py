from fastapi import Header, HTTPException
from app.db import tokens_collection, usages_collection
from datetime import datetime, timezone


async def get_current_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid authorization header")

    token_value = authorization.split(" ")[1]
    token_doc = await tokens_collection.find_one({"token": token_value})

    return token_doc


async def get_current_admin_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid authorization header")

    token_value = authorization.split(" ")[1]
    token_doc = await tokens_collection.find_one({"token": token_value})

    if not token_doc or not token_doc.get("isAdmin", False):
        raise HTTPException(
            status_code=403, detail="Admin privileges required")

    return token_doc


async def log_usage(token: str, endpoint: str):
    await usages_collection.insert_one(
        {
            "token": token,
            "endpoint": endpoint,
            "timestamp": datetime.now(timezone.utc),
        }
    )
