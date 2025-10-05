# services/pipeline_loader.py

import torch
from diffusers import (
    StableDiffusionControlNetPipeline, 
    ControlNetModel, 
    UniPCMultistepScheduler
)
from config import settings

# Cache the pipeline in a module-level variable to avoid reloading
_pipeline = None

def load_pipeline():
    """Load and return the ControlNet-enabled Stable Diffusion pipeline."""
    global _pipeline
    if _pipeline is None:
        # Load the ControlNet model (Canny) and the base Stable Diffusion model
        controlnet = ControlNetModel.from_pretrained(
            settings.CONTROLNET_MODEL_ID, torch_dtype=torch.float16
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            settings.BASE_MODEL_ID,
            controlnet=controlnet,
            safety_checker=None,  # disable safety checker if not needed
            torch_dtype=torch.float16
        )
        # Use UniPCMultistepScheduler for faster sampling as suggested in Diffusers docs
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        # Move pipeline to GPU if available, else use CPU offloading
        if torch.cuda.is_available():
            pipe.to("cuda")
        else:
            pipe.enable_model_cpu_offload()
        # Try enabling xformers for efficient attention (optional)
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except Exception:
            pass
        _pipeline = pipe
    return _pipeline
