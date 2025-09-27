import asyncio
from datetime import datetime
import pytest
from uuid6 import uuid7

import prontia.db.cosmosdb as db
from prontia.dto.conversation import (
    ConversationRequest,
    UpdateConversationRequest,
)
from prontia.dto.message import (
    CompletionMessageRequest,
    MessageRequest,
)
from prontia.models.conversation import Conversation
from prontia.models.message import Message

import prontia.services.chat as target

from tests.test_const import TEST_OWNER_ID


@pytest.fixture(
    scope="function",
    autouse=True,
)
def clear_container() -> None:
    container_name = "conversations"
    partition_path = "/owner_id"
    query = "SELECT * FROM c WHERE c.owner_id=@owner_id"
    parameters = [
        dict(name="@owner_id", value=TEST_OWNER_ID),
    ]

    items = asyncio.run(
        db._query_container(
            name=container_name,
            path=partition_path,
            query=query,
            parameters=parameters,
        ),
    )

    for item in items:
        asyncio.run(
            db._delete_item(
                item_id=item["id"],
                partition_key=item["owner_id"],
                container_name=container_name,
                partition_path=partition_path,
            ),
        )


@pytest.fixture
def conversation_1() -> Conversation:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    res = asyncio.run(
        db.upsert_conversation(
            conversation=conv,
        ),
    )
    return res


@pytest.fixture
def conversation_2() -> Conversation:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    asyncio.run(
        db.upsert_conversation(
            conversation=conv,
        ),
    )
    msg1 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
        role="user",
        content=f"私のIDは {id} です。",
    )
    asyncio.run(
        db.upsert_message(
            message=msg1,
        ),
    )

    msg2 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
        role="assistant",
        content="質問や問い合わせがあればお答えします。",
    )
    asyncio.run(
        db.upsert_message(
            message=msg2,
        ),
    )
    return conv


@pytest.mark.asyncio
async def test_get_hiostories_1() -> None:
    res = await target.get_hiostories(
        owner_id=TEST_OWNER_ID,
    )
    assert len(res) == 0


@pytest.mark.asyncio
async def test_get_hiostories_2(
    conversation_1,
) -> None:
    res = await target.get_hiostories(
        owner_id=TEST_OWNER_ID,
    )
    assert len(res) == 1
    assert res[0].id == conversation_1.id
    assert res[0].title == conversation_1.title


@pytest.mark.asyncio
async def test_start_conversation() -> None:
    req = CompletionMessageRequest(
        content="こんにちは",
    )

    start_at = datetime.now()
    res = await target.start_conversation(
        owner_id=TEST_OWNER_ID,
        request=req,
    )
    end_at = datetime.now()

    assert res.id is not None
    assert res.conversation_id is not None
    assert res.role == "assistant"
    assert res.content != ""

    conv = await db.get_conversation(
        id=res.conversation_id,
        owner_id=TEST_OWNER_ID,
    )

    assert conv is not None
    assert conv.id == res.conversation_id
    assert conv.owner_id == TEST_OWNER_ID
    assert conv.title is not None
    assert conv.created_at is not None
    assert conv.updated_at is not None
    assert conv.deleted_at is None
    assert conv.created_at == conv.updated_at
    assert conv.created_at > start_at
    assert conv.created_at < end_at

    msgs = await db.get_messages(
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
    )

    assert len(msgs) == 2
    assert msgs[0].id != res.id
    assert msgs[0].conversation_id == res.conversation_id
    assert msgs[0].role == "user"
    assert msgs[0].content == req.content
    assert msgs[0].created_at is not None
    assert msgs[0].updated_at is not None
    assert msgs[0].deleted_at is None
    assert msgs[0].created_at == msgs[0].updated_at
    assert msgs[0].created_at > start_at
    assert msgs[0].created_at < end_at

    assert msgs[1].id == res.id
    assert msgs[1].conversation_id == res.conversation_id
    assert msgs[1].role == res.role
    assert msgs[1].content == res.content
    assert msgs[1].created_at is not None
    assert msgs[1].updated_at is not None
    assert msgs[1].deleted_at is None
    assert msgs[1].created_at == msgs[1].updated_at
    assert msgs[1].created_at > start_at
    assert msgs[1].created_at < end_at


@pytest.mark.asyncio
async def test_get_conversation(
    conversation_1,
) -> None:
    req = ConversationRequest(
        id=conversation_1.id,
    )
    res = await target.get_conversation(
        owner_id=TEST_OWNER_ID,
        request=req,
    )

    assert res.id == conversation_1.id
    assert res.title == conversation_1.title


@pytest.mark.asyncio
async def test_update_conversation_title(
    conversation_1,
) -> None:
    title = str(uuid7())
    req = UpdateConversationRequest(
        id=conversation_1.id,
        title=title,
    )
    res = await target.update_conversation_title(
        owner_id=TEST_OWNER_ID,
        request=req,
    )

    assert res.id == conversation_1.id
    assert res.title == title

    conv = await db.get_conversation(
        id=res.id,
        owner_id=TEST_OWNER_ID,
    )

    assert conv is not None
    assert conv.id == conversation_1.id
    assert conv.owner_id == TEST_OWNER_ID
    assert conv.title != conversation_1.title
    assert conv.title == title
    assert conv.created_at == conversation_1.created_at
    assert conv.updated_at != conversation_1.updated_at
    assert conv.updated_at > conversation_1.updated_at
    assert conv.deleted_at is None


@pytest.mark.asyncio
async def test_delete_conversation(
    conversation_2,
) -> None:
    req = ConversationRequest(
        id=conversation_2.id,
    )
    await target.delete_conversation(
        owner_id=TEST_OWNER_ID,
        request=req,
    )

    conv = await db.get_conversation(
        id=conversation_2.id,
        owner_id=TEST_OWNER_ID,
    )

    assert conv is None

    msgs = await db.get_messages(
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_2.id,
    )

    assert len(msgs) == 0


@pytest.mark.asyncio
async def test_get_conversation_messages(
    conversation_2,
) -> None:
    req = MessageRequest(
        conversation_id=conversation_2.id,
    )
    msgs = await target.get_conversation_messages(
        owner_id=TEST_OWNER_ID,
        request=req,
    )

    assert len(msgs) == 2
    for msg in msgs:
        assert msg.id is not None
        assert msg.conversation_id == conversation_2.id
        assert msg.role is not None
        assert msg.content is not None


@pytest.mark.asyncio
async def test_completion_messages(
    conversation_2,
) -> None:
    req = CompletionMessageRequest(
        conversation_id=conversation_2.id,
        content="私のIDは何ですか？",
    )
    msg = await target.completion_messages(
        owner_id=TEST_OWNER_ID,
        request=req,
    )

    assert msg.id is not None
    assert msg.conversation_id == conversation_2.id
    assert msg.role == "assistant"
    assert msg.content != ""

    msgs = await db.get_messages(
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_2.id,
    )

    assert len(msgs) == 3
    for msg in msgs:
        assert msg.id is not None
        assert msg.conversation_id == conversation_2.id
        assert msg.role is not None
        assert msg.content is not None
