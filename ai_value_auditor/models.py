# ai_value_auditor/models.py
"""
Data models for the AI Value Auditor system.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class Task(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

class Message(BaseModel):
    role: str  # 'human' or 'ai'
    content: str
    timestamp: Optional[datetime] = None

class Conversation(BaseModel):
    task_id: int
    messages: List[Message]

class RiskyResponse(BaseModel):
    id: int
    task_id: int
    message: str
    response: str
    reason: str
    timestamp: datetime

class AIIncident(BaseModel):
    id: int
    title: str
    description: str
    date: str
    category: str
    source: Optional[str] = None

