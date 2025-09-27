from uuid6 import uuid7
from typing import List

from prontia.db import cosmosdb as db
from prontia.dto.message import (
    MessageRequest,
    MessageResponse,
    CompletionMessageRequest,
)
from prontia.dto.conversation import (
    ConversationRequest,
    ConversationResponse,
    UpdateConversationRequest,
)
from prontia.models.conversation import Conversation
from prontia.models.message import Message
from prontia.services.openai import (
    generate_title,
    completion,
)


async def get_hiostories(
    owner_id: str,
) -> List[ConversationResponse]:
    convs = await db.get_conversations(
        owner_id=owner_id,
    )

    history = [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
        )
        for conv in convs
    ]
    return history


async def start_conversation(
    owner_id: str,
    request: CompletionMessageRequest,
) -> MessageResponse:
    request.conversation_id = str(uuid7())
    title = await generate_title(
        content=request.content,
    )
    conv = Conversation(
        id=request.conversation_id,
        owner_id=owner_id,
        title=title,
    )
    req_msg = Message(
        id=str(uuid7()),
        owner_id=owner_id,
        conversation_id=conv.id,
        role="user",
        content=request.content,
    )

    conv = await db.upsert_conversation(
        conversation=conv,
    )
    req_msg = await db.upsert_message(
        message=req_msg,
    )

    msg = await completion(
        owner_id=owner_id,
        conversation_id=conv.id,
        messages=req_msg,
    )

    res_msg = await db.upsert_message(
        message=msg,
    )

    res = MessageResponse(
        id=res_msg.id,
        conversation_id=res_msg.conversation_id,
        role=res_msg.role,
        content=res_msg.content,
    )
    return res


async def get_conversation(
    owner_id: str,
    request: ConversationRequest,
) -> ConversationResponse:
    conv = await db.get_conversation(
        id=request.id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    res = ConversationResponse(
        id=conv.id,
        title=conv.title,
    )
    return res


async def update_conversation_title(
    owner_id: str,
    request: UpdateConversationRequest,
) -> ConversationResponse:
    conv = await db.get_conversation(
        id=request.id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    conv.title = request.title
    conv_res = await db.upsert_conversation(
        conversation=conv,
    )
    res = ConversationResponse(
        id=conv_res.id,
        title=conv_res.title,
    )
    return res


async def delete_conversation(
    owner_id: str,
    request: ConversationRequest,
) -> None:
    conv = await db.get_conversation(
        id=request.id,
        owner_id=owner_id,
    )

    if conv is None:
        raise ValueError("Conversation not found")

    await db.delete_conversation(
        converation=conv,
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
    request: MessageRequest,
) -> List[MessageResponse]:
    msgs = await db.get_messages(
        owner_id=owner_id,
        conversation_id=request.conversation_id,
    )

    res = [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
        )
        for msg in msgs
    ]
    return res


async def completion_messages(
    owner_id: str,
    request: CompletionMessageRequest,
) -> MessageResponse:
    if request.conversation_id is None:
        raise ValueError("conversation_id is required")

    msgs = await db.get_messages(
        owner_id=owner_id,
        conversation_id=request.conversation_id,
    )
    req_msg = Message(
        id=str(uuid7()),
        owner_id=owner_id,
        conversation_id=request.conversation_id,
        role="user",
        content=request.content,
    )

    res_msg = await completion(
        owner_id=owner_id,
        conversation_id=request.conversation_id,
        messages=req_msg,
        history=msgs,
    )

    msg = await db.upsert_message(
        message=res_msg,
    )

    res = MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
    )
    return res
