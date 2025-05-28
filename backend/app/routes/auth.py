from fastapi import APIRouter, Depends, HTTPException, status
from app.db import tokens_collection
from app.models import Token, TokenRequest
from app.dependencies import get_current_admin_token
from app.dependencies import log_usage
from typing import List
from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/tokens", response_model=List[Token])
async def get_tokens(admin_token=Depends(get_current_admin_token)):
    await log_usage(admin_token, "/auth/tokens")

    tokens_cursor = tokens_collection.find()
    tokens = await tokens_cursor.to_list(length=100)
    return tokens


@router.post(
    "/tokens",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
async def add_token(token_data: TokenRequest,
                    admin_token=Depends(get_current_admin_token)):
    await log_usage(admin_token, "/auth/tokens")

    existing = await tokens_collection.find_one({"token": token_data.token})
    if existing:
        raise HTTPException(status_code=400, detail="Token already exists")

    token_doc = {
        "token": token_data.token,
        "isAdmin": token_data.isAdmin,
        "createdAt": datetime.now(timezone.utc),
    }
    await tokens_collection.insert_one(token_doc)
    return token_doc


@router.delete("/tokens/{token}", status_code=204)
async def delete_token(
    token: str, 
    admin_token=Depends(get_current_admin_token),
):
    await log_usage(admin_token, "/auth/tokens")

    result = await tokens_collection.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
