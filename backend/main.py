from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS (Allows frontend or iOS app to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "AI Education Assistant is running!"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use latest GPT model
            messages=[{"role": "user", "content": request.question}],
            max_tokens=150
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

