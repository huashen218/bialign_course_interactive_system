
# ai_value_auditor/database.py
"""
Database implementation for the AI Value Auditor system.
This is a simple in-memory database for demonstration purposes.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import json

from .models import Task, Conversation, Message, RiskyResponse, AIIncident

class Database:
    """Simple in-memory database for the AI Value Auditor system."""
    
    def __init__(self):
        self.tasks = {}
        self.conversations = {}
        self.risky_responses = []
        self.ai_incidents = []
        self.next_task_id = 1
        self.next_risky_id = 1
        self.next_incident_id = 1
    
    def has_data(self) -> bool:
        """Check if database has any data."""
        return len(self.tasks) > 0
    
    def create_sample_data(self):
        """Create sample data for demonstration."""
        # Add sample tasks
        for i in range(1, 5):
            self.tasks[i] = {
                "id": i,
                "title": f"Sample Task {i}",
                "description": f"This is a sample task {i} for demonstration.",
                "created_at": datetime.now()
            }
            self.conversations[i] = []
            
        # Add sample AI incidents
        self.ai_incidents = [
            {
                "id": 1,
                "title": "Content Filter Bypass",
                "description": "An AI assistant was prompted to generate harmful content through a clever bypass technique.",
                "date": "2023-09-15",
                "category": "Safety",
                "source": "https://example.com/incident1"
            },
            {
                "id": 2,
                "title": "Biased Recommendations",
                "description": "An AI system showed gender bias in job recommendation algorithms.",
                "date": "2023-07-22",
                "category": "Fairness",
                "source": "https://example.com/incident2"
            }
        ]
        
        self.next_task_id = 5
        self.next_incident_id = 3
        
    def get_tasks(self) -> List[Task]:
        """Get all tasks."""
        return [Task(**task) for task in self.tasks.values()]
    
    def get_conversation(self, task_id: int) -> List[Message]:
        """Get conversation for a task."""
        if task_id not in self.conversations:
            return []
        return [Message(**msg) for msg in self.conversations[task_id]]
    
    def add_message(self, task_id: int, role: str, content: str):
        """Add a message to a conversation."""
        if task_id not in self.conversations:
            self.conversations[task_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        }
        
        self.conversations[task_id].append(message)
        return Message(**message)
    
    def add_risky_response(self, task_id: int, message: str, response: str, reason: str) -> RiskyResponse:
        """Record a risky response."""
        risky = {
            "id": self.next_risky_id,
            "task_id": task_id,
            "message": message,
            "response": response,
            "reason": reason,
            "timestamp": datetime.now()
        }
        
        self.risky_responses.append(risky)
        self.next_risky_id += 1
        
        return RiskyResponse(**risky)
    
    def get_risky_responses(self) -> List[RiskyResponse]:
        """Get all risky responses."""
        return [RiskyResponse(**risky) for risky in self.risky_responses]
    
    def get_ai_incidents(self) -> List[AIIncident]:
        """Get all AI incidents."""
        return [AIIncident(**incident) for incident in self.ai_incidents]

