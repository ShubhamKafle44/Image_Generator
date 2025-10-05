"""
app.py — main FastAPI entry point
Run with:
    uvicorn app:app --reload
"""

from fastapi import FastAPI
from routes import router  # import routes.py

# Initialize app
app = FastAPI(
    title="Prompt + Image Guided Diffusion API",
    version="1.0",
    description="Stable Diffusion v1.5 + ControlNet (Canny) backend"
)

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to the Prompt + Image Guided Diffusion API"}

# Include all routes from routes.py
app.include_router(router)
