from typing import List

from pydantic import BaseModel


class PromptContent(BaseModel):
    type: str
    text: str


class Prompt(BaseModel):
    role: str
    content: List[PromptContent]
