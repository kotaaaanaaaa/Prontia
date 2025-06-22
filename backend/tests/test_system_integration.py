import pytest

from app.api import conversation as target


@pytest.mark.asyncio
async def test_new_conversation() -> None:
    res = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    assert res.id is not None
    assert res.conversation_id is not None
    assert res.role == 'assistant'
    assert res.content is not None


@pytest.mark.asyncio
async def test_conversation_history() -> None:
    msg1 = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    msg2 = await target.start_conversation(
        user='test_user',
        content='hello',
    )

    convs = await target.get_history(
        user='test_user',
    )
    res = [conv.id for conv in convs]
    assert msg1.conversation_id in res
    assert msg2.conversation_id in res


@pytest.mark.asyncio
async def test_get_conversation() -> None:
    msg = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    res = await target.get_conversation(
        user='test_user',
        id=msg.conversation_id,
    )
    assert res.id is not None
    assert res.title is not None


@pytest.mark.asyncio
async def test_delete_conversation() -> None:
    msg = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    await target.delete_conversation(
        user='test_user',
        id=msg.conversation_id,
    )

    with pytest.raises(Exception):
        await target.get_conversation(
            user='test_user',
            id=msg.conversation_id,
        )


@pytest.mark.asyncio
async def test_get_conversation_messages() -> None:
    msg = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    res = await target.get_conversation_messages(
        user='test_user',
        id=msg.conversation_id,
    )
    assert len(res) >= 1


@pytest.mark.asyncio
async def test_continue_conversation_1() -> None:
    res_1 = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    res_2 = await target.send_question(
        id=res_1.conversation_id,
        content='what can you do?',
        user='test_user',
    )
    assert res_2.id is not None
    assert res_2.conversation_id == res_1.conversation_id
    assert res_2.role == 'assistant'
    assert res_2.content is not None


@pytest.mark.asyncio
async def test_continue_conversation_2() -> None:
    res_1 = await target.start_conversation(
        user='test_user',
        content='Today is January 1, 2025, and the weather is cloudy.',
    )
    res_2 = await target.send_question(
        id=res_1.conversation_id,
        content="Please tell me today's date and weather",
        user='test_user',
    )
    assert res_2.id is not None
    assert res_2.conversation_id == res_1.conversation_id
    assert res_2.role == 'assistant'
    assert res_2.content is not None
