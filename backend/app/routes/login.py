from fastapi import APIRouter, HTTPException, status
from app.models import TokenRequest
from app.db import tokens_collection

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/verify-token")
async def verify_token(data: TokenRequest):
    token_doc = await tokens_collection.find_one({"token": data.token})
    if not token_doc:
        raise HTTPException(status_code=404, detail="Token not found")

    if token_doc.get("isAdmin") != data.isAdmin:
        raise HTTPException(status_code=403, detail="Token role mismatch")

    return {"message": "Token is valid"}
