from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

load_dotenv()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI / NexusAI Client
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://apidev.navigatelabsai.com"
)

# Request Model
class PromptRequest(BaseModel):
    user_prompt: str

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "NexusAI is working"}

# Welcome Endpoint
@app.get("/welcome/")
def welcome():
    return {"message": "Welcome to Navi Chat"}

# AI Endpoint
@app.post("/run_task/")
async def run_task(req: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a personal AI tutor. "
                        "Explain things in simple layman terms. "
                        "Keep responses short and precise. "
                        "Do not hallucinate."
                    )
                },
                {
                    "role": "user",
                    "content": req.user_prompt
                }
            ]
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}