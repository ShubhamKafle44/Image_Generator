from fastapi import FastAPI
from src.database import engine, Base
from src.routers import generate, results
import sys
import os

# --- Add project root to Python path so "api" can be imported ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ---------------------------------------------------------------


from fastapi import FastAPI
from src.routers import generate, results

app = FastAPI(
    title="ControlNet Canny Image Generator",
    description="Generates images via Stable Diffusion conditioned on Canny edges."
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(generate.router, prefix="/api")
app.include_router(results.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "ControlNet Canny Image Generator API is running!"}
