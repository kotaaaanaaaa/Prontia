from pydantic import BaseModel


class ConversationResponse(BaseModel):
    id: str
    title: str


class StartConversationRequest(BaseModel):
    content: str


class QuestionRequest(BaseModel):
    content: str
