from datetime import datetime

import pytest
from uuid6 import uuid7

from prontia.db import cosmosdb as target
from prontia.models.conversation import Conversation
from prontia.models.message import Message

from tests.test_const import TEST_OWNER_ID


@pytest.mark.asyncio
async def test_basic_conversation() -> None:
    id = str(uuid7())
    dt = datetime.now()

    expect = Conversation(
        id=id,
        owner_id=TEST_OWNER_ID,
        title="New Chat",
    )

    create = await target.upsert_conversation(
        conversation=expect,
    )
    assert id == create.id
    assert create.created_at is not None
    assert dt <= create.created_at
    assert create.updated_at is not None
    assert dt <= create.updated_at

    reads = await target.get_conversations(
        owner_id=TEST_OWNER_ID,
    )
    assert len(reads) > 0

    read = await target.get_conversation(
        id=id,
        owner_id=TEST_OWNER_ID,
    )
    assert read is not None
    assert id == read.id
    assert create.created_at is not None
    assert read.created_at == create.updated_at
    assert create.updated_at is not None
    assert read.updated_at == create.updated_at

    await target.delete_conversation(
        conv=create,
    )

    read = await target.get_conversation(
        id=id,
        owner_id=TEST_OWNER_ID,
    )
    assert read is None


@pytest.mark.asyncio
async def test_basic_message() -> None:
    id = str(uuid7())
    conversation_id = str(uuid7())
    dt = datetime.now()

    expect = Message(
        id=id,
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
        role="user",
        content="Hello, world!",
    )

    create = await target.upsert_message(
        message=expect,
    )
    assert id == create.id
    assert conversation_id == create.conversation_id
    assert create.created_at is not None
    assert dt <= create.created_at
    assert create.updated_at is not None
    assert dt <= create.updated_at

    reads = await target.get_messages(
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
    )
    assert len(reads) > 0

    read = await target.get_message(
        id=id,
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
    )
    assert read is not None
    assert id == read.id
    assert create.created_at is not None
    assert read.created_at == create.updated_at
    assert create.updated_at is not None
    assert read.created_at == create.updated_at

    await target.delete_message(
        message=create,
    )

    read = await target.get_message(
        id=id,
        owner_id=TEST_OWNER_ID,
        conversation_id=conversation_id,
    )
    assert read is None
