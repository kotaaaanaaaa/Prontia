import pytest
from uuid6 import uuid7

from prontia.models.message import Message
from prontia.services import openai as target

from tests.test_const import TEST_OWNER_ID


def test_create_completion() -> None:
    messages = [
        target.get_system_prompt(),
        target.Prompt(
            role="user",
            content=[
                target.PromptContent(
                    type="text",
                    text="こんにちは",
                ),
            ],
        ),
    ]

    res = target.create_completion(
        messages=messages,
    )
    assert res.created is not None
    assert res.id is not None
    assert res.model is not None
    assert len(res.choices) > 0
    assert res.choices[0].message.role != ""
    assert res.choices[0].message.content != ""


@pytest.mark.asyncio
async def test_completion_1() -> None:
    conversation_id = str(uuid7())
    message = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        role="user",
        content="こんにちは",
    )
    res = await target.completion(
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        messages=message,
    )
    assert res.conversation_id == conversation_id
    assert res.id != message.id
    assert res.role != ""
    assert res.content != ""


@pytest.mark.asyncio
async def test_completion_2() -> None:
    conversation_id = str(uuid7())
    id = str(uuid7())
    msg1 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        role="user",
        content=f"私のIDは {id} です。",
    )

    msg2 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        role="assistant",
        content="質問や問い合わせがあればお答えします。",
    )

    msg = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        role="user",
        content="私のIDは何ですか？",
    )

    res = await target.completion(
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        messages=msg,
        history=[msg1, msg2],
    )

    assert id in res.content
