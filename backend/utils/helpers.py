# utils/helpers.py

import numpy as np
import cv2
from PIL import Image
from config import settings

def apply_canny(image: Image.Image) -> Image.Image:
    """
    Apply Canny edge detection to the input PIL image and return a 3-channel PIL image of edges.
    """
    # Convert PIL image to NumPy array (RGB)
    image_np = np.array(image)
    # Convert to grayscale for Canny
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    # Apply Canny edge detector using thresholds from settings
    edges = cv2.Canny(
        gray, 
        settings.CANNY_LOW_THRESHOLD, 
        settings.CANNY_HIGH_THRESHOLD
    )
    # Stack to create 3 channels (ControlNet expects 3-channel input)
    edges_3ch = np.stack([edges]*3, axis=-1)
    # Convert back to PIL Image
    canny_image = Image.fromarray(edges_3ch)
    return canny_image
