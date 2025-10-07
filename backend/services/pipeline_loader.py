
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["XFORMERS_DISABLED"] = "1"
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import torch
def load_txt2img_pipeline():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5"
    )
    pipe.to("cpu")  # force CPU
    return pipe

def load_img2img_pipeline():
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5"
    )
    pipe.to("cpu")  # force CPU
    return pipe
