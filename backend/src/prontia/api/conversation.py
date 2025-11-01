from fastapi import APIRouter, Depends
from typing import List

from prontia.dto.conversation import (
    ConversationResponse,
    StartConversationRequest,
    QuestionRequest,
)
from prontia.dto.message import (
    MessageResponse,
)
from prontia.services.user import get_user
from prontia.services import chat as service


router = APIRouter(prefix="/conversations")


@router.get("")
async def get_histories(
    owner_id=Depends(get_user),
) -> List[ConversationResponse]:
    convs = await service.get_histories(
        owner_id=owner_id,
    )

    res = [
        ConversationResponse(
            id=conv.id,
            title=conv.title,
        )
        for conv in convs
    ]
    return res


@router.get("/{id}")
async def get_conversation(
    id: str,
    owner_id=Depends(get_user),
) -> ConversationResponse:
    conv = await service.get_conversation(
        owner_id=owner_id,
        id=id,
    )
    res = ConversationResponse(
        id=conv.id,
        title=conv.title,
    )
    return res


@router.delete("/{id}")
async def delete_conversation(
    id: str,
    owner_id=Depends(get_user),
) -> None:
    await service.delete_conversation(
        owner_id=owner_id,
        id=id,
    )


@router.get("/{id}/messages")
async def get_conversation_messages(
    id: str,
    owner_id=Depends(get_user),
) -> List[MessageResponse]:
    msgs = await service.get_conversation_messages(
        owner_id=owner_id,
        id=id,
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


@router.post("/message")
async def start_conversation(
    req: StartConversationRequest,
    owner_id=Depends(get_user),
) -> MessageResponse:
    msg = await service.start_conversation(
        owner_id=owner_id,
        content=req.content,
    )

    res = MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
    )
    return res


@router.post("/{id}/message")
async def send_question(
    id: str,
    req: QuestionRequest,
    owner_id=Depends(get_user),
) -> MessageResponse:
    msg = await service.completion_message(
        owner_id=owner_id,
        id=id,
        content=req.content,
    )
    res = MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
    )
    return res
