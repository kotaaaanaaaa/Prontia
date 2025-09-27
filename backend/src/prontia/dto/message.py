from pydantic import BaseModel


class MessageRequest(BaseModel):
    conversation_id: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str


class CompletionMessageRequest(BaseModel):
    conversation_id: str | None = None
    content: str
