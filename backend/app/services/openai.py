from openai import AzureOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from pydantic import BaseModel
from typing import List

from app.core.logging import log
from app.core.settings import settings


class PromptContent(BaseModel):
    type: str
    text: str


class Prompt(BaseModel):
    role: str
    content: List[PromptContent]


def completion(
        messages: List[Prompt]
) -> ChatCompletion:
    client = AzureOpenAI(
        azure_endpoint=settings.openai.ENDPOINT,
        api_key=settings.openai.APIKEY,
        api_version="2025-01-01-preview",
    )

    msgs = [message.model_dump() for message in messages]
    response = client.chat.completions.create(
        model=settings.openai.DEPLOYMENT,
        messages=msgs,
        max_tokens=800,
        temperature=1.0,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )
    result = ChatCompletion.model_validate(response)

    return result


def prepare_messages(
        system: Prompt,
        message: Prompt,
        history: List[Prompt],
) -> List[Prompt]:
    msgs: List[Prompt] = [system]

    if history:
        for msg in history[-5:]:
            msgs.append(msg)
    msgs.append(message)

    return msgs
