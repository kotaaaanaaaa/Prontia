from datetime import datetime

from pydantic import BaseModel


class Conversation(BaseModel):
    id: str
    owner_id: str
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
