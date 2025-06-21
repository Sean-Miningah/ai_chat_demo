from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
db = client[os.getenv("DATABASE_NAME", "ai_chat")]
collection = db[os.getenv("COLLECTION_NAME", "questions")]

class Question(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    response: str

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(question_data: Question):
    try:
        document = {
            "question": question_data.question,
            "timestamp": datetime.now()
        }
        collection.insert_one(document)

        return QuestionResponse(response="Thanks for your question, I'll think about it.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Crewmind AI Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
