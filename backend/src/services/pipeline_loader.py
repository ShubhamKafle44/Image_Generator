import torch
from diffusers import (
    StableDiffusionPipeline, 
    StableDiffusionImg2ImgPipeline,
    DPMSolverMultistepScheduler
)
import os

# Cache pipelines to avoid reloading
_txt2img_pipeline = None
_img2img_pipeline = None

# Model configuration
MODEL_ID = "runwayml/stable-diffusion-v1-5"  # or "stabilityai/stable-diffusion-2-1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Only use float16 on CUDA, use float32 on CPU
if DEVICE == "cuda":
    TORCH_DTYPE = torch.float16
    print("Using CUDA with float16 for faster inference")
else:
    TORCH_DTYPE = torch.float32
    print("Using CPU with float32 (this will be slower)")

def load_txt2img_pipeline():
    """Load and cache text-to-image pipeline"""
    global _txt2img_pipeline
    
    if _txt2img_pipeline is None:
        print(f"Loading text-to-image pipeline on {DEVICE}...")
        
        try:
            # Load pipeline with appropriate dtype
            _txt2img_pipeline = StableDiffusionPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=TORCH_DTYPE,
                safety_checker=None,  # Disable safety checker for faster loading
                requires_safety_checker=False
            )
            
            # Use DPM++ solver for faster generation
            _txt2img_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                _txt2img_pipeline.scheduler.config
            )
            
            _txt2img_pipeline = _txt2img_pipeline.to(DEVICE)
            
            # Enable memory optimizations only for GPU
            if DEVICE == "cuda":
                _txt2img_pipeline.enable_attention_slicing()
                try:
                    # Optional: enable xformers for even faster generation if available
                    _txt2img_pipeline.enable_xformers_memory_efficient_attention()
                    print("xformers memory efficient attention enabled")
                except Exception:
                    print("xformers not available, using standard attention")
            
            print("✓ Text-to-image pipeline loaded successfully!")
            
        except Exception as e:
            print(f"✗ Error loading text-to-image pipeline: {e}")
            raise
    
    return _txt2img_pipeline


def load_img2img_pipeline():
    """Load and cache image-to-image pipeline"""
    global _img2img_pipeline
    
    if _img2img_pipeline is None:
        print(f"Loading image-to-image pipeline on {DEVICE}...")
        
        try:
            # Load pipeline with appropriate dtype
            _img2img_pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
                MODEL_ID,
                torch_dtype=TORCH_DTYPE,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            # Use DPM++ solver for faster generation
            _img2img_pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
                _img2img_pipeline.scheduler.config
            )
            
            _img2img_pipeline = _img2img_pipeline.to(DEVICE)
            
            # Enable memory optimizations only for GPU
            if DEVICE == "cuda":
                _img2img_pipeline.enable_attention_slicing()
                try:
                    _img2img_pipeline.enable_xformers_memory_efficient_attention()
                    print("xformers memory efficient attention enabled")
                except Exception:
                    print("xformers not available, using standard attention")
            
            print("✓ Image-to-image pipeline loaded successfully!")
            
        except Exception as e:
            print(f"✗ Error loading image-to-image pipeline: {e}")
            raise
    
    return _img2img_pipeline


def unload_pipelines():
    """Unload pipelines to free memory"""
    global _txt2img_pipeline, _img2img_pipeline
    
    if _txt2img_pipeline is not None:
        del _txt2img_pipeline
        _txt2img_pipeline = None
    
    if _img2img_pipeline is not None:
        del _img2img_pipeline
        _img2img_pipeline = None
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    print("Pipelines unloaded and cache cleared")


# Test function
if __name__ == "__main__":
    print(f"Device: {DEVICE}")
    print(f"Torch dtype: {TORCH_DTYPE}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    
    try:
        pipe = load_txt2img_pipeline()
        print("✓ Text-to-image pipeline loaded successfully")
        
        # Test generation with appropriate steps for CPU/GPU
        steps = 500 if DEVICE == "cuda" else 50  # Fewer steps on CPU
        print(f"Generating test image with {steps} steps...")
        
        output = pipe(
            "a beautiful sunset",
            num_inference_steps=steps,
            guidance_scale=7.5
        )
        print(f"✓ Test image generated: {output.images[0].size}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()