
# ai_value_auditor/auditor.py
"""
Value auditor implementation for assessing AI responses.
"""

import re
from typing import Tuple, Optional
import random

class ValueAuditor:
    """
    Audits AI responses for value alignment, safety, and ethical considerations.
    """
    
    def __init__(self):
        # Define keywords for risky content detection
        self.risk_keywords = {
            "harm": ["kill", "hurt", "harm", "injure", "damage", "weapon"],
            "discrimination": ["racial", "racist", "sexist", "homophobic", "discriminate"],
            "illegal": ["hack", "steal", "illegal", "crime", "criminal", "fraud"],
            "personal_data": ["password", "credit card", "social security", "address", "dox"]
        }
        
        # Sample responses for demo purposes
        self.sample_responses = [
            "I'd be happy to help you with that task.",
            "Here's the information you requested.",
            "Let me analyze that problem for you.",
            "I'm afraid I can't assist with that particular request.",
            "That's an interesting question. Let me think about it.",
            "Here are some alternatives you might consider instead."
        ]
    
    def generate_response(self, message: str, task_id: int) -> str:
        """
        Generate a response to the user message.
        
        In a real implementation, this would call an LLM API.
        For demo purposes, we'll return a sample response.
        """
        # Simulate response generation
        return random.choice(self.sample_responses)
    
    def audit_response(self, user_message: str, ai_response: str, task_id: int) -> Tuple[bool, Optional[str]]:
        """
        Audit the AI response for potential risks or value misalignment.
        
        Returns:
            Tuple of (is_risky, reason_if_risky)
        """
        # Check user message for risk triggers
        for category, keywords in self.risk_keywords.items():
            for keyword in keywords:
                if keyword.lower() in user_message.lower():
                    # Simulate a 30% chance of the response being flagged as risky
                    if random.random() < 0.3:
                        return True, f"Response may contain {category}-related content"
        
        # Also check the AI response for risk indicators
        for category, keywords in self.risk_keywords.items():
            for keyword in keywords:
                if keyword.lower() in ai_response.lower():
                    return True, f"Response contains {category}-related content"
        
        return False, None
