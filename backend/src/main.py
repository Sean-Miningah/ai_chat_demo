from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import List, Optional
from openai import OpenAI

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

llm_url = os.getenv("LLM_URL", "https://api.openai.com/v1/chat/completions")
llm_model = os.getenv("LLM_Model", "gpt-3.5-turbo")
class Question(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    response: str
    timestamp: datetime

class HistoryItem(BaseModel):
    question: str
    response: str
    timestamp: datetime

class HistoryResponse(BaseModel):
    history: List[HistoryItem]
    total_count: int

# Function to generate dynamic response using LLM model API
async def generate_ai_response(question: str) -> str:
    open_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(
        base_url=llm_url,
        api_key=open_api_key
    )

    if not open_api_key:
        return generate_dummy_response(question)

    try:
        completion = client.chat.completions.create(
            extra_body={},
            model=llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Provide concise and helpful responses."},
                {"role": "user", "content": question}
            ]
        )
        if completion and completion.choices and completion.choices[0].message.content:
            return completion.choices[0].message.content
        else:
            return generate_dummy_response(question)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return generate_dummy_response(question)

def generate_dummy_response(question: str) -> str:
    question_lower = question.lower()

    if any(word in question_lower for word in ["hello", "hi", "hey"]):
        return "Hello! How can I help you today?"
    else:
        return f"Thanks for sharing that with me. I've received your message: '{question[:50]}...' and I'll consider it carefully."


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(question_data: Question):
    try:

        # Generate dynamic response
        ai_response = await generate_ai_response(question_data.question)

        print("The ai response here is", ai_response)
        current_time = datetime.now()

        document = {
            "question": question_data.question,
            "response": ai_response,
            "timestamp": current_time
        }

        collection.insert_one(document)

        return QuestionResponse(
            response=ai_response,
            timestamp=current_time
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/recent")
async def get_recent_history(count: int = 10):
    try:
        count = min(count, 50)

        cursor = collection.find({}).sort("timestamp", -1).limit(count)

        recent_items = []
        for doc in cursor:
            recent_items.append({
                "question": doc["question"],
                "response": doc.get("response", "No response recorded"),
                "timestamp": doc["timestamp"]
            })

        return {"recent_history": recent_items}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history", response_model=HistoryResponse)
async def get_history(limit: Optional[int] = 50, skip: Optional[int] = 0):
    try:
        limit = min(limit if limit is not None else 100, 100)

        total_count = collection.count_documents({})

        # Get history items sorted by timestamp (newest first)
        cursor = collection.find({}).sort("timestamp", -1).skip(skip if skip is not None else 0).limit(limit)

        history_items = []
        for doc in cursor:
            history_items.append(HistoryItem(
                question=doc["question"],
                response=doc.get("response", "No response recorded"),
                timestamp=doc["timestamp"]
            ))

        return HistoryResponse(
            history=history_items,
            total_count=total_count
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    try:
        total_questions = collection.count_documents({})

        first_question = collection.find({}).sort("timestamp", 1).limit(1)
        first_timestamp = None
        for doc in first_question:
            first_timestamp = doc["timestamp"]
            break

        latest_question = collection.find({}).sort("timestamp", -1).limit(1)
        latest_timestamp = None
        for doc in latest_question:
            latest_timestamp = doc["timestamp"]
            break

        return {
            "total_questions": total_questions,
            "first_question_at": first_timestamp,
            "latest_question_at": latest_timestamp,
            "database_name": db.name,
            "collection_name": collection.name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Crewmind AI Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
