from pydantic import BaseModel


class ConversationRequest(BaseModel):
    id: str


class ConversationResponse(BaseModel):
    id: str
    title: str


class UpdateConversationRequest(BaseModel):
    id: str
    title: str
