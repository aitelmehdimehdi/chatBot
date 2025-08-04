from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import os
from openai import OpenAI
from dotenv import load_dotenv

app = FastAPI()

# Serve static files under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = []

@app.get("/", response_class=HTMLResponse)
async def read_index():
    return pathlib.Path("static/index.html").read_text(encoding="utf-8")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    reply = f"You said: {user_message}"


    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    messages = [
        { 
            "role" : "system" ,
            "content" : "You are a smart assistant who answer for what asked for exactly and gives only short answers with exactly what the user ask for , and your name is MAYLEN",
            }
        ]

    messages.append(
        {
            "role":"user",
            "content":user_message
        }
    )

    response = client.chat.completions.create(
        model= "deepseek/deepseek-r1-0528:free",
        messages=messages
    )

    result = response.choices[0].message.content

    print(f" Assistant : {result}")

    messages.append(
        {
            "role":"assitant",
            "content":result
        }
    )



    print("Received message:", user_message)
    print("Replying with:", result)

    chat_history.append({"user": user_message, "bot": result})
    return {"reply": result}
