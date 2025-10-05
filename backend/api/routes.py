"""
routes.py — contains routes and model logic for the Prompt + Image Guided Diffusion API
"""

import io
import torch
import numpy as np
import cv2
from PIL import Image
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler
)

# Create a router (to be included in app.py)
router = APIRouter()

# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------
def get_device_and_dtype():
    """Determine whether to use GPU or CPU."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float16 if device.type == "cuda" else torch.float32
    return device, dtype


def preprocess_image(input_pil: Image.Image, low_thresh=100, high_thresh=200, size=512):
    """Convert a PIL image to a 3-channel Canny edge PIL image."""
    input_pil = input_pil.convert("RGB").resize((size, size))
    np_img = np.array(input_pil)
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, low_thresh, high_thresh)
    edges_3ch = np.stack([edges, edges, edges], axis=2)
    return Image.fromarray(edges_3ch)


# ----------------------------------------------------------
# Load model (only once)
# ----------------------------------------------------------
print("🔄 Loading Stable Diffusion + ControlNet (Canny)...")

device, dtype = get_device_and_dtype()

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-canny", torch_dtype=dtype
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=dtype,
)

pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_attention_slicing()

if device.type == "cuda":
    pipe = pipe.to(device)
    try:
        pipe.enable_xformers_memory_efficient_attention()
    except Exception:
        pass

print("✅ Model ready.")

# ----------------------------------------------------------
# Routes
# ----------------------------------------------------------
@router.get("/health")
async def health_check():
    """Quick API health check."""
    return {"status": "ok", "device": str(device), "dtype": str(dtype)}


@router.post("/generate")
async def generate_image(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    negative_prompt: str = Form(""),
    steps: int = Form(30),
    guidance: float = Form(7.5),
    seed: int = Form(42)
):
    """
    Generate image from text + image using Stable Diffusion ControlNet (Canny).
    """
    try:
        contents = await file.read()
        input_pil = Image.open(io.BytesIO(contents)).convert("RGB")

        control_img = preprocess_image(input_pil)

        generator = torch.Generator(device=device).manual_seed(seed)

        with torch.inference_mode():
            output = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt.strip() else None,
                image=control_img,
                num_inference_steps=steps,
                guidance_scale=guidance,
                generator=generator
            )

        result = output.images[0]

        # Convert to PNG stream
        img_bytes = io.BytesIO()
        result.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return StreamingResponse(img_bytes, media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
