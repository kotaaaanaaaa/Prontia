from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Conversation(BaseModel):
    user_id: str
    id: str
    type: str = 'conversation'
    title: Optional[str] = 'New Chat'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Message(BaseModel):
    user_id: str
    id: str
    type: str = 'message'
    conversation_id: str
    role: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
