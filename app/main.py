from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.models.database import init_db
from app.routes import router

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Personalized workout & nutrition plans powered by Google Gemini AI",
    version="1.0.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routes
app.include_router(router)
