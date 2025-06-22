from fastapi import APIRouter, Depends
from typing import List

from app.core.logging import log
from app.models.request import ConversationResponse, MessageResponse
from app.services import conversation as srv_conv
from app.services.user import get_user


router = APIRouter(prefix='/conversations')


@router.get('/')
async def get_history(
    user=Depends(get_user),
) -> List[ConversationResponse]:
    '''

    '''
    convs = await srv_conv.get_conversations(
        user_id=user,
    )
    results: List[ConversationResponse] = []
    for conv in convs:
        results.append(
            ConversationResponse(
                id=conv.id,
                title=conv.title,
            )
        )
    return results


@router.get('/{id}')
async def get_conversation(
    id: str,
    user=Depends(get_user),
) -> ConversationResponse:
    '''

    '''
    conv = await srv_conv.get_conversation(
        id=id,
        user_id=user,
    )
    result = ConversationResponse(
        id=conv.conversation_id,
        title=conv.title,
    )
    return result


@router.delete('/{id}')
async def delete_conversation(
    id: str,
    user=Depends(get_user),
) -> None:
    '''

    '''
    srv_conv.delete_conversation(
        user_id=user,
        id=id,
    )


@router.get('/{id}/messages/')
async def get_conversation_messages(
    id: str,
    user=Depends(get_user),
) -> List[MessageResponse]:
    '''

    '''
    msgs = await srv_conv.get_messages(
        user_id=user,
        conversation_id=id,
    )
    results: List[MessageResponse] = []
    for msg in msgs:
        results.append(
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
            )
        )
    return results


@router.post('/message/')
async def start_conversation(
    content: str,
    user=Depends(get_user),
) -> MessageResponse:
    '''

    '''
    conv = await srv_conv.create_conversation(
        user_id=user,
    )
    msg = await srv_conv.insert_message(
        user_id=user,
        conversation_id=conv.id,
        content=content,
    )

    res = await srv_conv.send_message(
        user_id=user,
        conversation_id=conv.id,
        message=msg,
    )
    result = MessageResponse(
        id=res.id,
        conversation_id=res.conversation_id,
        role=res.role,
        content=res.content,
    )
    return result


@router.post('/{id}/message/')
async def send_question(
    id: str,
    content: str,
    user=Depends(get_user),
) -> MessageResponse:
    '''

    '''
    history = await srv_conv.get_messages(
        user_id=user,
        conversation_id=id,
    )
    msg = await srv_conv.insert_message(
        user_id=user,
        conversation_id=id,
        content=content,
    )

    res = await srv_conv.send_message(
        user_id=user,
        conversation_id=id,
        message=msg,
        history=history
    )
    result = MessageResponse(
        id=res.id,
        conversation_id=res.conversation_id,
        role=res.role,
        content=res.content,
    )
    return result
