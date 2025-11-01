from uuid6 import uuid7
from typing import List

from prontia.db import cosmosdb as db
from prontia.models.conversation import Conversation
from prontia.models.message import Message
from prontia.services import openai


async def get_histories(
    owner_id: str,
) -> List[Conversation]:
    convs = await db.get_conversations(
        owner_id=owner_id,
    )
    return convs


async def start_conversation(
    owner_id: str,
    content: str,
) -> tuple[Message, Message]:
    id = str(uuid7())
    title = await openai.generate_title(
        content=content,
    )
    conv = Conversation(
        id=id,
        owner_id=owner_id,
        title=title,
    )
    req = Message(
        id=str(uuid7()),
        owner_id=owner_id,
        conversation_id=conv.id,
        role="user",
        content=content,
    )

    await db.upsert_conversation(
        conversation=conv,
    )
    await db.upsert_message(
        message=req,
    )

    msg = await openai.completion(
        owner_id=owner_id,
        conversation_id=conv.id,
        messages=req,
    )

    res = await db.upsert_message(
        message=msg,
    )
    return req, res


async def get_conversation(
    owner_id: str,
    id: str,
) -> Conversation:
    conv = await db.get_conversation(
        id=id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    return conv


async def update_conversation_title(
    owner_id: str,
    id: str,
    title: str,
) -> Conversation:
    conv = await db.get_conversation(
        id=id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    conv.title = title
    res = await db.upsert_conversation(
        conversation=conv,
    )
    return res


async def delete_conversation(
    owner_id: str,
    id: str,
) -> None:
    conv = await db.get_conversation(
        id=id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    await db.delete_conversation(
        conversation=conv,
    )
    msgs = await db.get_messages(
        owner_id=owner_id,
        conversation_id=conv.id,
    )
    for msg in msgs:
        await db.delete_message(
            message=msg,
        )


async def get_conversation_messages(
    owner_id: str,
    id: str,
) -> List[Message]:
    msgs = await db.get_messages(
        owner_id=owner_id,
        conversation_id=id,
    )

    return msgs


async def completion_message(
    owner_id: str,
    id: str,
    content: str,
) -> tuple[Message, Message]:
    msgs = await db.get_messages(
        owner_id=owner_id,
        conversation_id=id,
    )
    req = Message(
        id=str(uuid7()),
        owner_id=owner_id,
        conversation_id=id,
        role="user",
        content=content,
    )

    res = await openai.completion(
        owner_id=owner_id,
        conversation_id=id,
        messages=req,
        history=msgs,
    )

    await db.upsert_message(
        message=res,
    )
    return req, res
