
# ai_value_auditor/server.py
"""
FastAPI server implementation for the AI Value Auditor system.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
import json
import os
from pathlib import Path

from .auditor import ValueAuditor
from .models import Task, Conversation, Message, RiskyResponse, AIIncident
from .database import Database

app = FastAPI(title="AI Value Auditor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and auditor
db = Database()
auditor = ValueAuditor()

# API Models
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
    is_risky: bool
    risk_reason: Optional[str] = None

# Routes
@app.get("/api/tasks", response_model=List[Task])
async def get_tasks():
    return db.get_tasks()

@app.get("/api/conversations/{task_id}", response_model=List[Message])
async def get_conversation(task_id: int):
    conversation = db.get_conversation(task_id)
    if not conversation:
        raise HTTPException(status_code=404, detail=f"Conversation for task {task_id} not found")
    return conversation

@app.post("/api/conversations/{task_id}/messages", response_model=MessageResponse)
async def send_message(task_id: int, message_req: MessageRequest):
    # Store user message
    db.add_message(task_id, "human", message_req.message)
    
    # Generate AI response
    ai_response = auditor.generate_response(message_req.message, task_id)
    
    # Audit the response
    is_risky, risk_reason = auditor.audit_response(message_req.message, ai_response, task_id)
    
    # Store AI response
    db.add_message(task_id, "ai", ai_response)
    
    # If risky, record it
    if is_risky:
        db.add_risky_response(task_id, message_req.message, ai_response, risk_reason)
    
    return {
        "response": ai_response,
        "is_risky": is_risky,
        "risk_reason": risk_reason
    }

@app.get("/api/risky-responses", response_model=List[RiskyResponse])
async def get_risky_responses():
    return db.get_risky_responses()

@app.get("/api/ai-incidents", response_model=List[AIIncident])
async def get_ai_incidents():
    return db.get_ai_incidents()

# Serve static files in production
@app.on_event("startup")
async def startup_event():
    # Create sample data if database is empty
    if not db.has_data():
        db.create_sample_data()

# Add this near the end of the file, before the start_server function
app.mount("/", StaticFiles(directory="/Users/huashen/Dropbox/333_1_workspace/projects/4.202504-valueauditor/ai-value-auditor-frontend/build", html=True), name="static")

def start_server(host="0.0.0.0", port=8000, reload=False):
    """Start the FastAPI server"""
    uvicorn.run("ai_value_auditor.server:app", host=host, port=port, reload=reload)
