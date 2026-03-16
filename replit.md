# FitBuddy – AI Fitness Plan Generator

## Overview
A personalized workout and nutrition plan generator powered by Google Gemini AI. Users enter their profile (name, age, weight, fitness goal, intensity) and receive a custom 7-day workout plan plus nutrition tips. Plans can be refined through a feedback loop.

## Tech Stack
- **Framework:** FastAPI (Python)
- **Server:** Uvicorn (port 5000)
- **Database:** SQLite via SQLAlchemy (fitbuddy.db)
- **AI:** Google Gemini 2.0 Flash via `google-generativeai`
- **Templates:** Jinja2
- **Frontend:** Static HTML/CSS/JS served by FastAPI

## Project Structure
```
run.py              # Entry point — starts Uvicorn on port 5000
app/
  main.py           # FastAPI app setup, static files, DB init
  routes/
    routes.py       # Web routes (home, generate, feedback, all_users)
    ai_service.py   # Gemini AI integration (workout plan, nutrition, regenerate)
  models/
    database.py     # SQLAlchemy models (User, WorkoutPlan) + SQLite setup
  templates/        # Jinja2 HTML templates
  static/           # CSS and JS assets
```

## Environment Variables / Secrets
- `GEMINI_API_KEY` — Google Gemini API key (required for AI plan generation)

## Running the App
```bash
python run.py
```
App runs on `http://0.0.0.0:5000`

## Deployment
Configured for autoscale deployment:
```
uvicorn app.main:app --host=0.0.0.0 --port=5000
```
