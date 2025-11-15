from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
from openai import OpenAI

app = FastAPI()

# Serve static files and templates
app.mount("/static", StaticFiles(directory="html"), name="static")
templates = Jinja2Templates(directory="html")

# OpenAI client
client = OpenAI(api_key="", timeout=600)

def ask_gpt(prompt: str, system_prompt: Optional[str] = None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages
    )
    return response.choices[0].message.content

# Index page
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Recipes GET (initial load)
@app.get("/recipies", response_class=HTMLResponse)
def recipies_page(request: Request):
    return templates.TemplateResponse("recipies.html", {"request": request, "gpt_response": None})

# Recipes POST (generate recipe)
@app.post("/recipies", response_class=HTMLResponse)
def generate_recipe(
    request: Request,
    restric: str = Form(...),
    fridge: str = Form(...),
    genre: str = Form(...),
    servings: int = Form(...)
):
    prompt = (
        f"Generate a recipe with dietary restrictions: {restric}, "
        f"ingredients available: {fridge}, cuisine: {genre}, servings: {servings}. "
        "Format: Recipe Name -> Ingredients -> Equipment -> Instructions. Clear spacing and no extra text."
    )
    system_prompt = "You are a helpful diet assistant."
    gpt_response = ask_gpt(prompt, system_prompt)

    return templates.TemplateResponse("recipies.html", {"request": request, "gpt_response": gpt_response})

@app.get("/workout", response_class=HTMLResponse)
def workout_page(request: Request):
    return templates.TemplateResponse("workout.html", {"request": request})

# Demo submit from homepage
@app.post("/submit", response_class=HTMLResponse)
def submit(
    request: Request,
    Name: str = Form(...),
    gender: str = Form(...),
    age: str = Form(...),
    height: str = Form(...),
    weight: str = Form(...),
    issues: str = Form(None)
):
    prompt = (
        f"Provide personalized diet and workout advice for:\n"
        f"Name: {Name}, Gender: {gender}, Age: {age}, Height: {height}, Weight: {weight}, Issues: {issues}"
    )
    system_prompt = "You are a helpful health assistant."
    gpt_response = ask_gpt(prompt, system_prompt)
    return HTMLResponse(f"<h1>Diet Buddy GPT Response</h1><pre>{gpt_response}</pre><a href='/'>Go back</a>")

@app.get("/workout", response_class=HTMLResponse)
def workout_page(request: Request):
    return templates.TemplateResponse(
        "workout.html",
        {"request": request, "workout_response": None}
    )

# Workout POST (generate workout)
@app.post("/workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    burn_goal: str = Form(...),
    workouttype: str = Form(...),
    difficulty: str = Form(...),
    time: str = Form(...)
):
    prompt = (
        f"Generate a workout plan with calorie burn goal: {burn_goal}, "
        f"type: {workouttype}, difficulty: {difficulty}, time: {time}. "
        "Format: Exercise -> Sets/Reps/Duration -> Instructions. Clear spacing and no extra text."
    )
    system_prompt = "You are a helpful personal trainer."
    workout_response = ask_gpt(prompt, system_prompt)

    return templates.TemplateResponse(
        "workout.html",
        {"request": request, "workout_response": workout_response}
    )

@app.get("/forum", response_class=HTMLResponse)
def workout_page(request: Request):
    return templates.TemplateResponse(
        "forum.html",
        {"request": request, "forum_response": None}
    )

@app.get("/login", response_class=HTMLResponse)
def workout_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "login_response": None}
    )