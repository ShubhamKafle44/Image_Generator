from fastapi import APIRouter, Header, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4
import io
from PIL import Image
import traceback

from src.database import get_db
from src.services.s3_service import upload_image
from src.models.result import Result
from ..services.pipeline_loader import load_txt2img_pipeline, load_img2img_pipeline
from utils.helpers import apply_canny
from config import settings

router = APIRouter()

@router.post("/generate", responses={200: {"content": {"image/png": {}}}})
async def generate_image(
    user_id: str = Header(...),
    db: Session = Depends(get_db),
    prompt: str = Form(...),
    image_file: UploadFile = File(None),
    use_canny: bool = Form(False),
    strength: float = Form(0.75),
    num_inference_steps: int = Form(settings.DEFAULT_INFERENCE_STEPS),
    guidance_scale: float = Form(settings.DEFAULT_GUIDANCE_SCALE)
):
    try:
        # --- Validate parameters ---
        num_inference_steps = max(1, min(int(num_inference_steps), 150))
        guidance_scale = max(1.0, min(float(guidance_scale), 30.0))
        strength = max(0.0, min(float(strength), 1.0))

        # --- Generate image ---
        if image_file is None:
            # Text-to-image
            pipe = load_txt2img_pipeline()
            out = pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                negative_prompt="blurry, low quality, distorted",
            )
            original_image_bytes = None
        else:
            # Image-to-image
            image_bytes = await image_file.read()
            try:
                input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                max_size = 1024
                if max(input_image.size) > max_size:
                    input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

            original_image_bytes = image_bytes
            if use_canny:
                input_image = apply_canny(input_image)

            pipe = load_img2img_pipeline()
            out = pipe(
                prompt=prompt,
                image=input_image,
                strength=strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                negative_prompt="blurry, low quality, distorted",
            )

        if hasattr(out, 'images') and len(out.images) > 0:
            generated_image = out.images[0]
        else:
            raise Exception("Pipeline did not return any images")

        # --- Convert generated image to bytes ---
        buf = io.BytesIO()
        generated_image.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        gen_bytes = buf.getvalue()

        # --- Create transaction folder ---
        transaction_id = str(uuid4())
        orig_key = gen_key = None
        orig_url = gen_url = None

        # Original image upload
        if original_image_bytes is not None:
            orig_key, orig_url = upload_image(
                original_image_bytes,
                user_id,
                transaction_id,
                "original"
            )

        gen_key, gen_url = upload_image(
            gen_bytes,
            user_id,
            transaction_id,
            "generated"
        )

        # --- Save to DB ---
        new_result = Result(
            id=str(uuid4()),
            user_id=user_id,
            prompt=prompt,
            original_s3_key=orig_key,
            original_image_url=orig_url,
            generated_s3_key=gen_key,
            generated_image_url=gen_url,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)

        return Response(
            content=gen_bytes,
            media_type="image/png",
            headers={
                "X-Inference-Steps": str(num_inference_steps),
                "X-Guidance-Scale": str(guidance_scale)
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        print(f"Error: {tb}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "trace": tb
}
        )
