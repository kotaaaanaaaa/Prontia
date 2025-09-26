from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: str
    owner_id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
