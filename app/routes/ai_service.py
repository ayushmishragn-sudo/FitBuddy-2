import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

AI_ERROR_QUOTA = "__QUOTA_ERROR__"
AI_ERROR_GENERIC = "__AI_ERROR__"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_model(model_name: str = "gemini-2.5-flash"):
    return genai.GenerativeModel(model_name)


def generate_workout_plan(name: str, age: int, weight: str, goal: str, intensity: str) -> str:
    """Generate a personalized 7-day workout plan using Gemini AI."""
    model = get_model()

    prompt = f"""
You are a professional fitness coach. Create a detailed, personalized 7-day workout plan for the following person:

- Name: {name}
- Age: {age} years old
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

OUTPUT FORMAT — follow this EXACTLY. Do not add any extra text, headers, or markdown outside this structure.

DAY 1 - [Focus Name]
WARMUP: [5–10 min light cardio description, e.g. marching in place, arm circles]
1. [Exercise Name] – [sets] sets of [reps/duration]
2. [Exercise Name] – [sets] sets of [reps/duration]
3. [Exercise Name] – [sets] sets of [reps/duration]
4. [Exercise Name] – [sets] sets of [reps/duration]
5. [Exercise Name] – [sets] sets of [reps/duration]
COOLDOWN: [5 min static stretching description]
---
DAY 2 - [Focus Name]
WARMUP: [description]
1. [Exercise] – [sets x reps]
2. [Exercise] – [sets x reps]
3. [Exercise] – [sets x reps]
4. [Exercise] – [sets x reps]
5. [Exercise] – [sets x reps]
COOLDOWN: [description]
---
[Repeat exactly the same pattern for DAY 3 through DAY 7]

Rules:
- Each day MUST start with "DAY N - Focus Name" on its own line.
- WARMUP: line comes right after the day title.
- Exercises are numbered 1–5, each on its own line.
- COOLDOWN: line comes after exercise 5.
- Days are separated by a line containing only "---".
- Do NOT include any text before DAY 1 or after the last COOLDOWN line.
- Keep exercises bodyweight-friendly and appropriate for {intensity} intensity.
- Tailor every exercise choice to the {goal} goal.
- Create unique workouts for all 7 days.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower():
            return AI_ERROR_QUOTA
        return AI_ERROR_GENERIC


def generate_nutrition_tip(goal: str) -> str:
    """Generate a nutrition/recovery tip based on fitness goal."""
    model = get_model()

    prompt = f"""
You are a certified nutritionist. Provide concise, practical nutrition and recovery advice for someone with the fitness goal: {goal}

OUTPUT FORMAT — follow this EXACTLY. Use these exact labels on their own lines:

NUTRITION: [2–3 specific, comma-separated nutrition recommendations tailored to {goal}]
HYDRATION: [1–2 clear hydration tips]
RECOVERY: [1–2 practical recovery tips, e.g. sleep, stretching, rest days]
QUICKTIP: [One powerful, bold, actionable tip — maximum 20 words]

Rules:
- Each section starts with its label (NUTRITION:, HYDRATION:, RECOVERY:, QUICKTIP:) followed by the content on the same line.
- Do NOT add any other text, headers, or markdown outside these 4 lines.
- Keep total response under 150 words.
- Be specific to the {goal} goal.
"""

    try:
        time.sleep(1)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower():
            return AI_ERROR_QUOTA
        return AI_ERROR_GENERIC


def regenerate_plan_with_feedback(
    name: str, age: int, weight: str, goal: str, intensity: str,
    original_plan: str, feedback: str
) -> str:
    """Regenerate a workout plan based on user feedback."""
    model = get_model("gemini-2.5-flash")

    prompt = f"""
You are a professional fitness coach. A client has provided feedback on their workout plan and needs an updated version.

**Client Details:**
- Name: {name}
- Age: {age} years old
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

**Original Plan:**
{original_plan}

**Client Feedback:**
{feedback}

Please create an IMPROVED 7-day workout plan that specifically addresses the feedback while maintaining the original goal.

OUTPUT FORMAT — follow this EXACTLY. Do not add any extra text, headers, or markdown outside this structure.

CHANGES: [One sentence explaining what was changed based on feedback]
DAY 1 - [Focus Name]
WARMUP: [5–10 min light cardio description]
1. [Exercise Name] – [sets] sets of [reps/duration]
2. [Exercise Name] – [sets] sets of [reps/duration]
3. [Exercise Name] – [sets] sets of [reps/duration]
4. [Exercise Name] – [sets] sets of [reps/duration]
5. [Exercise Name] – [sets] sets of [reps/duration]
COOLDOWN: [5 min static stretching description]
---
[Repeat the same DAY pattern for DAY 2 through DAY 7, each separated by ---]

Rules:
- Start with a single CHANGES: line, then immediately DAY 1.
- Each day starts with "DAY N - Focus Name".
- WARMUP: then 5 numbered exercises then COOLDOWN:.
- Separate days with a line containing only "---".
- No text after the last COOLDOWN line.
- Address the client's feedback: {feedback}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower():
            return AI_ERROR_QUOTA
        return AI_ERROR_GENERIC
