from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response, JSONResponse
from PIL import Image
import io
import traceback
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
    """
    Generate an image using Hugging Face Stable Diffusion models.
    
    Parameters:
    - prompt: Text description of the image to generate
    - image_file: Optional input image for img2img
    - use_canny: Apply canny edge detection to input image
    - strength: Strength for img2img (0-1, higher = more change)
    - num_inference_steps: Number of denoising steps (15-100 recommended)
    - guidance_scale: How closely to follow the prompt (1-20, 7.5 typical)
    """
    try:
        # Validate parameters
        num_inference_steps = max(1, min(int(num_inference_steps), 150))
        guidance_scale = max(1.0, min(float(guidance_scale), 30.0))
        strength = max(0.0, min(float(strength), 1.0))
        
        # Choose pipeline based on presence of image
        if image_file is None:
            # Text-to-Image generation
            pipe = load_txt2img_pipeline()
            
            # Generate image with explicit parameters
            out = pipe(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                negative_prompt="blurry, low quality, distorted",  # Optional default
            )
        else:
            # Image-to-Image generation
            pipe = load_img2img_pipeline()
            
            try:
                # Read and validate input image
                image_bytes = await image_file.read()
                input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                
                # Optional: Resize if image is too large
                max_size = 1024
                if max(input_image.size) > max_size:
                    input_image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
            except Exception as img_error:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid image file: {str(img_error)}"
                )
            
            # Apply canny edge detection if requested
            if use_canny:
                input_image = apply_canny(input_image)
            
            # Generate image with img2img
            out = pipe(
                prompt=prompt,
                image=input_image,
                strength=strength,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                negative_prompt="blurry, low quality, distorted",  # Optional default
            )
        
        # Extract generated image
        if hasattr(out, 'images') and len(out.images) > 0:
            generated_image = out.images[0]
        else:
            raise Exception("Pipeline did not return any images")
        
        # Convert to PNG bytes
        buf = io.BytesIO()
        generated_image.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        
        return Response(
            content=buf.getvalue(), 
            media_type="image/png",
            headers={
                "X-Inference-Steps": str(num_inference_steps),
                "X-Guidance-Scale": str(guidance_scale)
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Log and return detailed error
        tb = traceback.format_exc()
        print(f"Error generating image: {tb}")  # Server-side logging
        
        return JSONResponse(
            status_code=500, 
            content={
                "error": str(e), 
                "trace": tb if settings.DEBUG else "Enable DEBUG mode for trace"
            }
        )