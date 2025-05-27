from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.dependencies import log_usage
from app.dependencies import get_current_token

router = APIRouter(tags=["moderate"])

@router.post("/moderate")
async def moderate_image(
    image: UploadFile = File(...),
    token: str = Depends(get_current_token)
):
    await log_usage(token, "/moderate")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    image_bytes = await image.read()

    fake_response = {
        "safeSearch": {
            "adult": "UNKNOWN",
            "violence": "UNKNOWN",
            "racy": "UNKNOWN"
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return JSONResponse(content=fake_response)