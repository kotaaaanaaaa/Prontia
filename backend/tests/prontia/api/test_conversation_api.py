from pydantic import TypeAdapter

from fastapi.testclient import TestClient
import pytest
from pytest_mock.plugin import MockerFixture as Mocker
from uuid6 import uuid7

from prontia.app import app
from prontia.dto.conversation import ConversationResponse
from prontia.dto.message import MessageResponse
from prontia.dto.message import QuestionResponse
from prontia.models.conversation import Conversation
from prontia.models.message import Message
from prontia.services.user import DEFAULT_USER_ID

from tests.test_const import TEST_OWNER_ID

client = TestClient(app)


@pytest.mark.asyncio
def test_get_histories_1(
    mocker: Mocker,
) -> None:
    convs = [
        Conversation(
            id=str(uuid7()),
            owner_id=TEST_OWNER_ID,
            title=str(uuid7()),
        ),
        Conversation(
            id=str(uuid7()),
            owner_id=TEST_OWNER_ID,
            title=str(uuid7()),
        ),
    ]

    m = mocker.patch(
        "prontia.services.chat.get_histories",
        return_value=convs,
    )

    res = client.get("/conversations")

    assert res.status_code == 200
    assert m.call_count == 1
    m.assert_called_with(
        owner_id=DEFAULT_USER_ID,
    )
    expect = [
        ConversationResponse(
            **conv.model_dump(),
        ).model_dump()
        for conv in convs
    ]
    assert res.json() == expect


@pytest.mark.asyncio
def test_get_conversation_1(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    mocker.patch(
        "prontia.services.chat.get_conversation",
        return_value=conv,
    )

    res = client.get("/conversations/1")

    assert res.status_code == 200
    expect = ConversationResponse(
        **conv.model_dump(),
    ).model_dump()
    assert res.json() == expect


@pytest.mark.asyncio
def test_delete_conversation_1(
    mocker: Mocker,
) -> None:
    id = str(uuid7())
    m = mocker.patch(
        "prontia.services.chat.delete_conversation",
        return_value=None,
    )

    res = client.delete(f"/conversations/{id}")

    assert res.status_code == 200
    assert m.call_count == 1
    m.assert_called_with(
        id=id,
        owner_id=DEFAULT_USER_ID,
    )


@pytest.mark.asyncio
def test_get_conversation_messages_1(
    mocker: Mocker,
) -> None:
    id = str(uuid7())
    msgs = [
        Message(
            id=str(uuid7()),
            owner_id=TEST_OWNER_ID,
            conversation_id=id,
            role=str(uuid7()),
            content=str(uuid7()),
        ),
        Message(
            id=str(uuid7()),
            owner_id=TEST_OWNER_ID,
            conversation_id=id,
            role=str(uuid7()),
            content=str(uuid7()),
        ),
    ]

    m = mocker.patch(
        "prontia.services.chat.get_conversation_messages",
        return_value=msgs,
    )

    res = client.get(f"/conversations/{id}/messages")

    assert res.status_code == 200
    assert m.call_count == 1
    m.assert_called_with(
        id=id,
        owner_id=DEFAULT_USER_ID,
    )
    expect = [
        MessageResponse(
            **msg.model_dump(),
        ).model_dump()
        for msg in msgs
    ]
    assert res.json() == expect


@pytest.mark.asyncio
def test_start_conversation_1(
    mocker: Mocker,
) -> None:
    content = str(uuid7())
    msg = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=str(uuid7()),
        role=str(uuid7()),
        content=content,
    )

    m = mocker.patch(
        "prontia.services.chat.start_conversation",
        return_value=msg,
    )

    res = client.post(
        "/conversations/message",
        headers={"X-Token": "coneofsilence"},
        json={
            "content": content,
        },
    )

    assert res.status_code == 200
    assert m.call_count == 1
    m.assert_called_with(
        owner_id=DEFAULT_USER_ID,
        content=content,
    )
    expect = QuestionResponse(
        **msg.model_dump(),
    ).model_dump()
    assert res.json() == expect


@pytest.mark.asyncio
def test_send_question_1(
    mocker: Mocker,
) -> None:
    id = str(uuid7())
    content = str(uuid7())
    msg = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=id,
        role=str(uuid7()),
        content=content,
    )

    m = mocker.patch(
        "prontia.services.chat.completion_message",
        return_value=msg,
    )

    res = client.post(
        f"/conversations/{id}/message",
        json={
            "content": content,
        },
    )

    assert res.status_code == 200
    assert m.call_count == 1
    m.assert_called_with(
        owner_id=DEFAULT_USER_ID,
        id=id,
        content=content,
    )
    expect = QuestionResponse(
        **msg.model_dump(),
    ).model_dump()
    assert res.json() == expect
