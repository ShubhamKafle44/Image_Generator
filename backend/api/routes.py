from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response, JSONResponse
from PIL import Image
import io, traceback

from services.pipeline_loader import load_txt2img_pipeline, load_img2img_pipeline
from utils.helpers import apply_canny
from config import settings

router = APIRouter()

@router.post("/api/generate", responses={200: {"content": {"image/png": {}}}})
async def generate_image(
    prompt: str = Form(...),
    image_file: UploadFile = File(None),  # optional
    use_canny: bool = Form(False),
    strength: float = Form(0.75),
    num_inference_steps: int = Form(settings.DEFAULT_INFERENCE_STEPS),
    guidance_scale: float = Form(settings.DEFAULT_GUIDANCE_SCALE)
):
    try:
        # Choose pipeline based on presence of image
        if image_file is None:
            pipe = load_txt2img_pipeline()
            out = pipe(
                prompt=prompt,
                num_inference_steps=int(num_inference_steps),
                guidance_scale=float(guidance_scale)
            )
        else:
            pipe = load_img2img_pipeline()
            try:
                input_image = Image.open(image_file.file).convert("RGB")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid image file")

            if use_canny:
                input_image = apply_canny(input_image)

            out = pipe(
                prompt=prompt,
                image=input_image,
                strength=float(strength),
                num_inference_steps=int(num_inference_steps),
                guidance_scale=float(guidance_scale)
            )

        generated_image = out.images[0]
        buf = io.BytesIO()
        generated_image.save(buf, format="PNG")
        buf.seek(0)
        return Response(content=buf.getvalue(), media_type="image/png")

    except Exception as e:
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "trace": tb})
