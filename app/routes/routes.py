from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.database import get_db, User, WorkoutPlan
from app.routes.ai_service import (
    generate_workout_plan,
    generate_nutrition_tip,
    regenerate_plan_with_feedback,
    AI_ERROR_QUOTA,
    AI_ERROR_GENERIC,
)

AI_ERROR_MSG_QUOTA = (
    "The Gemini API quota has been exceeded. Free-tier keys have a limited number of "
    "requests per day. Please wait a few minutes and try again, or check your quota at "
    "https://ai.dev/rate-limit."
)
AI_ERROR_MSG_GENERIC = "The AI service returned an unexpected error. Please try again."

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    # Validate inputs
    if age < 10 or age > 100:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Please enter a valid age between 10 and 100."},
        )
    try:
        weight_val = float(weight)
        if weight_val < 20 or weight_val > 300:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Please enter a valid weight between 20 and 300 kg."},
        )

    # Save user to DB
    user = User(name=name, age=age, weight=weight, goal=goal, intensity=intensity)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate plan and tip via AI
    plan_content = generate_workout_plan(name, age, weight, goal, intensity)

    if plan_content in (AI_ERROR_QUOTA, AI_ERROR_GENERIC):
        db.delete(user)
        db.commit()
        error_msg = AI_ERROR_MSG_QUOTA if plan_content == AI_ERROR_QUOTA else AI_ERROR_MSG_GENERIC
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": error_msg},
        )

    nutrition_tip = generate_nutrition_tip(goal)
    if nutrition_tip in (AI_ERROR_QUOTA, AI_ERROR_GENERIC):
        nutrition_tip = None

    # Save plan to DB
    plan = WorkoutPlan(
        user_id=user.id,
        plan_content=plan_content,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "plan": plan,
            "plan_id": plan.id,
        },
    )


@router.post("/feedback/{plan_id}", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    plan_id: int,
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    user = db.query(User).filter(User.id == plan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not feedback.strip():
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "user": user,
                "plan": plan,
                "plan_id": plan.id,
                "error": "Please enter your feedback before submitting.",
            },
        )

    # Regenerate plan with feedback
    updated_plan_content = regenerate_plan_with_feedback(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
        original_plan=plan.plan_content,
        feedback=feedback,
    )

    if updated_plan_content in (AI_ERROR_QUOTA, AI_ERROR_GENERIC):
        error_msg = AI_ERROR_MSG_QUOTA if updated_plan_content == AI_ERROR_QUOTA else AI_ERROR_MSG_GENERIC
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "user": user, "plan": plan, "plan_id": plan.id, "error": error_msg},
        )

    # Update plan in DB
    plan.plan_content = updated_plan_content
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "plan": plan,
            "plan_id": plan.id,
            "feedback_success": True,
        },
    )


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()

    user_plans = []
    for user in users:
        user_plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_plans.append({"user": user, "plan": user_plan})

    total_users = len(users)
    goals = {}
    for user in users:
        goals[user.goal] = goals.get(user.goal, 0) + 1

    success = request.query_params.get("success")

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "user_plans": user_plans,
            "total_users": total_users,
            "goals": goals,
            "success": success,
        },
    )


@router.get("/plan/{plan_id}", response_class=HTMLResponse)
async def view_plan(request: Request, plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user = db.query(User).filter(User.id == plan.user_id).first()
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "user": user, "plan": plan, "plan_id": plan.id},
    )


@router.get("/admin/user/{user_id}/edit", response_class=HTMLResponse)
async def admin_edit_user_form(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "edit_user.html",
        {"request": request, "user": user},
    )


@router.post("/admin/user/{user_id}/edit", response_class=HTMLResponse)
async def admin_edit_user(
    request: Request,
    user_id: int,
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    errors = []
    if age < 10 or age > 100:
        errors.append("Please enter a valid age between 10 and 100.")
    try:
        weight_val = float(weight)
        if weight_val < 20 or weight_val > 300:
            raise ValueError
    except ValueError:
        errors.append("Please enter a valid weight between 20 and 300 kg.")

    if errors:
        return templates.TemplateResponse(
            "edit_user.html",
            {"request": request, "user": user, "errors": errors},
        )

    user.name = name
    user.age = age
    user.weight = weight
    user.goal = goal
    user.intensity = intensity
    db.commit()

    return RedirectResponse(url="/admin?success=User+updated+successfully", status_code=303)


@router.post("/admin/user/{user_id}/delete")
async def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).delete()
    db.delete(user)
    db.commit()

    return RedirectResponse(url="/admin?success=User+deleted+successfully", status_code=303)
