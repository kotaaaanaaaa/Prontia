from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str

class QuestionResponse(MessageResponse):
    req_id: str