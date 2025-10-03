from typing import List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class State(BaseModel):
    input: Optional[str] = None  # Patient's initial health topic request
    output: Optional[Dict[str, Any]] = None  # Tavily search results
    messages: List[BaseMessage] = []  # Conversation log
    summary: Optional[str] = None  # Patient-friendly summary of health info
    quiz_question: Optional[str] = None  # Generated quiz question
    user_answer: Optional[str] = None  # Patient's answer
    grade: Optional[str] = None  # Grade & feedback
    restart: Optional[bool] = None  # Whether to restart or exit
