# config/settings.py

# Hugging Face model identifiers
BASE_MODEL_ID = "runwayml/stable-diffusion-v1-5"
CONTROLNET_MODEL_ID = "lllyasviel/sd-controlnet-canny"

# Default generation parameters
DEFAULT_INFERENCE_STEPS = 20
DEFAULT_GUIDANCE_SCALE = 7.5

# ControlNet Canny thresholds (can be adjusted if needed)
CANNY_LOW_THRESHOLD = 100
CANNY_HIGH_THRESHOLD = 200
