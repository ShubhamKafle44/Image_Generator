# src/main.py

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="ControlNet Canny Image Generator",
    description="Generates images via Stable Diffusion conditioned on Canny edges."
)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
