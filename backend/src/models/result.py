# app/models/result.py
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from src.database import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, index=True)  # UUID string
    user_id = Column(String, index=True, nullable=False)

    prompt = Column(Text, nullable=True)

    # S3 keys and public URLs
    original_s3_key = Column(String, nullable=True)
    original_image_url = Column(String, nullable=True)

    generated_s3_key = Column(String, nullable=False)
    generated_image_url = Column(String, nullable=False)

    num_inference_steps = Column(Integer, nullable=True)
    guidance_scale = Column(Integer, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
