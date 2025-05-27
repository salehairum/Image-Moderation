# uvicorn app.main:app --reload --port 7000

from fastapi import FastAPI, Depends, HTTPException, Header
from app.db import tokens_collection
from app.models import Token
from datetime import datetime
from app.routes import auth
from app.routes import login

app = FastAPI()

app.include_router(auth.router)
app.include_router(login.router)

async def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token_value = authorization.split(" ")[1]
    token_doc = await tokens_collection.find_one({"token": token_value})
    if not token_doc:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return token_doc

@app.get("/test")
async def ping(token = Depends(get_token)):
    return {"msg": "Testing if admin connects!", "admin": token["isAdmin"]}
