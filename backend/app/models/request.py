from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    role: str
    name: str


class ConversationResponse(BaseModel):
    id: str
    title: str


class MessageRequest(BaseModel):
    conversation_id: str
    content: str


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
