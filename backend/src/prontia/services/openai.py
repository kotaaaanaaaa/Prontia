from openai import AzureOpenAI
from openai.types.chat import ChatCompletion
from uuid6 import uuid7
from typing import List

from prontia.core.settings import settings
from prontia.models.prompt import Prompt, PromptContent
from prontia.models.message import Message


async def completion(
    owner_id: str,
    conversation_id: str,
    messages: Message,
    history: List[Message] = [],
) -> Message:
    system = get_system_prompt()
    msgs = [system]

    for msg in history[-5:]:
        msgs.append(to_prompt(msg))
    msgs.append(to_prompt(messages))

    res_msg = create_completion(messages=msgs)
    role = res_msg.choices[0].message.role
    content = res_msg.choices[0].message.content

    if content is None:
        raise ValueError("Response content is None")

    res = Message(
        id=str(uuid7()),
        owner_id=owner_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    return res


def create_completion(
    messages: List[Prompt],
) -> ChatCompletion:
    client = AzureOpenAI(
        azure_endpoint=settings.openai.ENDPOINT,
        api_key=settings.openai.APIKEY,
        api_version="2025-01-01-preview",
    )

    msgs = [message.model_dump() for message in messages]
    response = client.chat.completions.create(
        model=settings.openai.DEPLOYMENT,
        messages=msgs,  # type: ignore[arg-type]
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


async def generate_title(
    content: str,
) -> str:
    return "New Chat"


def get_system_prompt() -> Prompt:
    prompt = Prompt(
        role="system",
        content=[
            PromptContent(
                type="text",
                text="情報を見つけるのに役立つ AI アシスタントです。",
            ),
        ],
    )
    return prompt


def to_prompt(
    message: Message,
) -> Prompt:
    prompt = Prompt(
        role=message.role,
        content=[
            PromptContent(
                type="text",
                text=message.content,
            ),
        ],
    )
    return prompt
