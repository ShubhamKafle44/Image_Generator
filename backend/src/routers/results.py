from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.models.result import Result
from src.database import get_db
from src.schemas.result import ResultResponse
from src.services.s3_service import get_presigned_url, fetch_s3_results, delete_user_results

router = APIRouter(prefix="/user", tags=["Results"])


@router.get("/results", response_model=list[ResultResponse])
async def get_results(db: Session = Depends(get_db)):
    results = db.query(Result).all()

    normalized = []
    for r in results:
        normalized.append({
            "id": r.id,
            "user_id": r.user_id,
            "prompt": r.prompt,
            "num_inference_steps": r.num_inference_steps,
            "guidance_scale": r.guidance_scale,
            "timestamp": r.timestamp,

            "original_image_url": get_presigned_url(r.original_s3_key),
            "generated_image_url": get_presigned_url(r.generated_s3_key),
        })

    return normalized


@router.delete("/results")
def clear_results(
    user_id: str = Query(...),
    db: Session = Depends(get_db)
):
    delete_user_results(user_id, db)
    return {"message": "All results cleared"}
