import os
os.environ["XFORMERS_DISABLED"] = "1"  # <- Add this at the very top

from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
from PIL import Image

# Load text-to-image pipeline
pipe_txt2img = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# Test text-to-image
out = pipe_txt2img(prompt="A fantasy landscape")
out.images[0].save("txt2img_test.png")

# Load image-to-image pipeline
pipe_img2img = StableDiffusionImg2ImgPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

# Test image-to-image
img = Image.new("RGB", (512, 512), color="red")
out2 = pipe_img2img(prompt="A fantasy castle", image=img, strength=0.75)
out2.images[0].save("img2img_test.png")
