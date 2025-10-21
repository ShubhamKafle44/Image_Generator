from fastapi import FastAPI
import sys
import os

# --- Add project root to Python path so "api" can be imported ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ---------------------------------------------------------------


from fastapi import FastAPI
from api.routes import router  # use full import path

app = FastAPI(
    title="ControlNet Canny Image Generator",
    description="Generates images via Stable Diffusion conditioned on Canny edges."
)

# Register routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "ControlNet Canny Image Generator API is running!"}
