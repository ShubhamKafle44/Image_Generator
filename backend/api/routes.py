# api/routes.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import Response
from PIL import Image
import io

from config import settings
from services.pipeline_loader import load_pipeline
from utils.helpers import apply_canny

router = APIRouter()

@router.post("/generate", responses={200: {"content": {"image/png": {}}}})
async def generate_image(
    prompt: str = Form(...),
    image_file: UploadFile = File(...),
    num_inference_steps: int = Form(settings.DEFAULT_INFERENCE_STEPS),
    guidance_scale: float = Form(settings.DEFAULT_GUIDANCE_SCALE)
):
    """
    Endpoint to generate an image from a text prompt and input image.
    """
    # Load image from upload into PIL
    input_image = Image.open(image_file.file).convert("RGB")
    # Preprocess: apply Canny edge detector
    canny_image = apply_canny(input_image)

    # Load or get cached pipeline
    pipe = load_pipeline()
    # Run the generation pipeline
    output = pipe(
        prompt,
        canny_image,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    )
    generated_image = output.images[0]  # take the first (and only) output image

    # Convert PIL image to PNG bytes
    buf = io.BytesIO()
    generated_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    # Return image bytes with correct media type
    return Response(content=byte_im, media_type="image/png")
