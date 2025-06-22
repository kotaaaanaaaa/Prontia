from uuid6 import uuid7
from typing import List

from app.core.logging import log
from app.db import cosmosdb as db
from app.models.data import Conversation, Message
from app.services.openai import Prompt, PromptContent, prepare_messages, completion


async def create_conversation(
        user_id: str,
) -> Conversation:
    conv = Conversation(
        id=str(uuid7()),
        user_id=user_id,
    )
    conv = await db.upsert_conversation(conversation=conv)
    return conv


async def get_conversations(
        user_id: str,
) -> List[Conversation]:
    convs = await db.get_conversations(
        user_id=user_id,
    )
    return convs


async def get_conversation(
        user_id: str,
        id: str,
) -> Conversation:
    conv = await db.get_conversation(
        user_id=user_id,
        id=id,
    )
    return conv


async def update_conversation_title(
        user_id: str,
        id: str,
        title: str,
):
    conv = await db.get_conversation(
        user_id=user_id,
        id=id,
    )
    conv.title = title
    conv = await db.upsert_conversation(
        conversation=conv,
    )
    return conv


async def delete_conversation(
        user_id: str,
        id: str,
) -> None:
    await db.delete_conversation(
        user_id=user_id,
        id=id,
    )
    await db.delete_messages(
        user_id=user_id,
        conversation_id=id,
    )


async def insert_message(
        user_id: str,
        conversation_id: str,
        content: str,
        role: str = 'user',
) -> Message:
    msg = Message(
        user_id=user_id,
        id=str(uuid7()),
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    await db.upsert_message(
        message=msg,
    )
    return msg


async def get_message(
        user_id: str,
        conversation_id: str,
        id: str,
) -> Message:
    msg = await db.get_message(
        user_id=user_id,
        conversation_id=conversation_id,
        message_id=id,
    )
    return msg


async def get_messages(
        user_id: str,
        conversation_id: str,
) -> List[Message]:
    msgs = await db.get_messages(
        user_id=user_id,
        conversation_id=conversation_id,
    )
    return msgs


def get_system_prompt() -> Prompt:
    prompt = Prompt(
        role="system",
        content=[
            PromptContent(type="text", text="情報を見つけるのに役立つ AI アシスタントです。")
        ]
    )
    return prompt


def to_prompt(
        message: Message,
) -> Prompt:
    prompt = Prompt(
        role=message.role,
        content=[PromptContent(type="text", text=message.content)]
    )
    return prompt


async def send_message(
        user_id: str,
        conversation_id: str,
        message: Message,
        history: List[Message] = None,
) -> Message:
    '''

    '''
    system_prompt = get_system_prompt()
    user_prompt = to_prompt(message)
    history_prompts: List[Prompt] = []
    if history:
        history_prompts = [to_prompt(msg) for msg in history]

    messages = prepare_messages(
        system=system_prompt,
        message=user_prompt,
        history=history_prompts,
    )
    res = completion(messages=messages)

    res_role = res.choices[0].message.role
    res_content = res.choices[0].message.content

    answer = Message(
        user_id=user_id,
        id=str(uuid7()),
        conversation_id=conversation_id,
        role=res_role,
        content=res_content,
    )
    await db.upsert_message(
        message=answer,
    )
    return answer
