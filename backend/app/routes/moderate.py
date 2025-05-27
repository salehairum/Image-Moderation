from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.dependencies import log_usage
from app.dependencies import get_current_token
from PIL import Image
from io import BytesIO
import torch
from open_clip import create_model_and_transforms, get_tokenizer

router = APIRouter(tags=["moderate"])

model, _, preprocess = create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
tokenizer = get_tokenizer('ViT-B-32')
model.eval()  

labels = ["explicit nudity", "graphic violence", "hate symbol", "self-harm", "extremist propaganda", "safe content"]

@router.post("/moderate")
async def moderate_image(
    image: UploadFile = File(...),
    token: str = Depends(get_current_token)
):
    await log_usage(token, "/moderate")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    image_bytes = await image.read()
    try:
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    image_input = preprocess(pil_image).unsqueeze(0) 
    
    text_tokens = tokenizer(labels)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)

        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarity = (image_features @ text_features.T).squeeze(0)

    results = {label: float(score.item()) for label, score in zip(labels, similarity)}

    response = {
        "scores": results,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    # fake_response = {
    #     "safeSearch": {
    #         "adult": "UNKNOWN",
    #         "violence": "UNKNOWN",
    #         "racy": "UNKNOWN"
    #     },
    #     "timestamp": datetime.now(timezone.utc).isoformat()
    # }

    return JSONResponse(content=response, status_code=200)