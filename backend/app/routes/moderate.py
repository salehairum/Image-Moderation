from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.dependencies import log_usage
from app.dependencies import get_current_token
import random


router = APIRouter(prefix="/moderate", tags=["moderate"])

labels = [
    "explicit nudity",
    "graphic violence",
    "hate symbol",
    "self-harm",
    "extremist propaganda",
    "safe content",
]


@router.post("/")
async def moderate_image(
    image: UploadFile = File(...), token: str = Depends(get_current_token)
):
    await log_usage(token, "/moderate")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    random_scores = [random.uniform(0, 1) for _ in labels]
    total = sum(random_scores)
    normalized_scores = [round(score / total, 3) for score in random_scores]

    results = dict(zip(labels, normalized_scores))

    response = {
        "scores": results,
        "timestamp": datetime.now(timezone.utc).isoformat()}

    return JSONResponse(content=response, status_code=200)
