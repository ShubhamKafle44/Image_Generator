# app/schemas/result.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResultBase(BaseModel):
    prompt: Optional[str]
    num_inference_steps: Optional[int]
    guidance_scale: Optional[float]

    original_image_url: Optional[str] = None
    generated_image_url: Optional[str] = None


class ResultCreate(ResultBase):
    # used internally
    id: str
    user_id: str
    original_s3_key: Optional[str] = None
    generated_s3_key: str
    generated_image_url: str


class ResultResponse(ResultBase):
    id: str
    user_id: str
    prompt: str
    original_image_url: Optional[str] = None
    generated_image_url: Optional[str] = None
    num_inference_steps: int
    guidance_scale: float
    timestamp: datetime

    class Config:
        orm_mode = True

