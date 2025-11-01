import pytest
from pytest_mock.plugin import MockerFixture as Mocker
from uuid6 import uuid7

from prontia.models.conversation import Conversation
from prontia.models.message import Message

import prontia.services.chat as target

from tests.test_const import TEST_OWNER_ID


@pytest.mark.asyncio
async def test_get_hiostories_1(
    mocker: Mocker,
) -> None:
    m = mocker.patch(
        "prontia.db.cosmosdb.get_conversations",
        return_value=[],
    )

    res = await target.get_histories(
        owner_id=TEST_OWNER_ID,
    )

    assert m.call_count == 1
    m.assert_called_with(
        owner_id=TEST_OWNER_ID,
    )

    assert len(res) == 0


@pytest.mark.asyncio
async def test_get_hiostories_2(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    m = mocker.patch(
        "prontia.db.cosmosdb.get_conversations",
        return_value=[conv],
    )

    res = await target.get_histories(
        owner_id=TEST_OWNER_ID,
    )

    assert m.call_count == 1
    m.assert_called_with(
        owner_id=TEST_OWNER_ID,
    )

    assert len(res) == 1
    assert res[0].id == conv.id
    assert res[0].title == conv.title


@pytest.mark.asyncio
async def test_get_hiostories_3(
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
        "prontia.db.cosmosdb.get_conversations",
        return_value=convs,
    )

    res = await target.get_histories(
        owner_id=TEST_OWNER_ID,
    )

    assert m.call_count == 1
    m.assert_called_with(
        owner_id=TEST_OWNER_ID,
    )

    assert len(res) == 2
    assert res[0].id == convs[0].id
    assert res[0].title == convs[0].title
    assert res[1].id == convs[1].id
    assert res[1].title == convs[1].title


@pytest.mark.asyncio
async def test_start_conversation_1(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    msg = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    content = "こんにちは"

    m1 = mocker.patch(
        "prontia.services.openai.generate_title",
        return_value=content,
    )
    m2 = mocker.patch(
        "prontia.db.cosmosdb.upsert_conversation",
        return_value=conv,
    )
    m3 = mocker.patch(
        "prontia.db.cosmosdb.upsert_message",
        return_value=msg,
    )
    m4 = mocker.patch(
        "prontia.services.openai.completion",
        return_value=msg,
    )

    req, res = await target.start_conversation(
        owner_id=TEST_OWNER_ID,
        content=content,
    )

    assert m1.call_count == 1
    m1.assert_called_with(
        content=content,
    )
    assert m2.call_count == 1
    _, m2_kwargs = m2.call_args
    assert m2_kwargs["conversation"].owner_id == TEST_OWNER_ID
    assert m2_kwargs["conversation"].title == content
    assert m3.call_count == 2
    m3_args = m3.call_args_list
    _, m3_kwargs = m3_args[0]
    assert m3_kwargs["message"].owner_id == TEST_OWNER_ID
    assert m3_kwargs["message"].conversation_id == m2_kwargs["conversation"].id
    assert m3_kwargs["message"].role == "user"
    assert m3_kwargs["message"].content == content
    _, m3_kwargs = m3_args[1]
    assert m3_kwargs["message"].owner_id == msg.owner_id
    assert m3_kwargs["message"].conversation_id == msg.conversation_id
    assert m3_kwargs["message"].role == msg.role
    assert m3_kwargs["message"].content == msg.content
    assert m4.call_count == 1
    _, m4_kwargs = m4.call_args
    assert m4_kwargs["owner_id"] == TEST_OWNER_ID
    assert m4_kwargs["conversation_id"] == m2_kwargs["conversation"].id
    assert m4_kwargs["messages"].owner_id == TEST_OWNER_ID
    assert m4_kwargs["messages"].conversation_id == m2_kwargs["conversation"].id
    assert m4_kwargs["messages"].role == "user"
    assert m4_kwargs["messages"].content == content
    assert m4_kwargs.get("history", None) is None

    assert res.id == msg.id
    assert res.conversation_id == msg.conversation_id
    assert res.role == msg.role
    assert res.content == msg.content

    assert req.id != msg.id
    assert req.conversation_id != msg.conversation_id
    assert req.role == "user"
    assert req.content == content


@pytest.mark.asyncio
async def test_get_conversation_1(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    m = mocker.patch(
        "prontia.db.cosmosdb.get_conversation",
        return_value=conv,
    )

    res = await target.get_conversation(
        id=conv.id,
        owner_id=TEST_OWNER_ID,
    )

    assert m.call_count == 1
    m.assert_called_with(
        id=conv.id,
        owner_id=TEST_OWNER_ID,
    )
    assert res.id == conv.id
    assert res.owner_id == conv.owner_id
    assert res.title == conv.title


@pytest.mark.asyncio
async def test_get_conversation_2(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    m = mocker.patch(
        "prontia.db.cosmosdb.get_conversation",
        return_value=None,
    )

    with pytest.raises(ValueError):
        await target.get_conversation(
            id=conv.id,
            owner_id=TEST_OWNER_ID,
        )

    assert m.call_count == 1
    m.assert_called_with(
        id=conv.id,
        owner_id=TEST_OWNER_ID,
    )


@pytest.mark.asyncio
async def test_update_conversation_title_1(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    title = str(uuid7())
    conv2 = Conversation(
        id=conv.id,
        owner_id=conv.owner_id,
        title=title,
    )
    m1 = mocker.patch(
        "prontia.db.cosmosdb.get_conversation",
        return_value=conv,
    )
    m2 = mocker.patch(
        "prontia.db.cosmosdb.upsert_conversation",
        return_value=conv2,
    )

    res = await target.update_conversation_title(
        owner_id=TEST_OWNER_ID,
        id=conv.id,
        title=title,
    )
    assert m1.call_count == 1
    m1.assert_called_with(
        id=conv.id,
        owner_id=TEST_OWNER_ID,
    )
    assert m2.call_count == 1
    _, m2_kwargs = m2.call_args
    assert m2_kwargs["conversation"].id == conv.id
    assert m2_kwargs["conversation"].owner_id == conv.owner_id
    assert m2_kwargs["conversation"].title == title

    assert res.id == conv.id
    assert res.owner_id == TEST_OWNER_ID
    assert res.title == title


@pytest.mark.asyncio
async def test_delete_conversation_1(
    mocker: Mocker,
) -> None:
    conv = Conversation(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        title=str(uuid7()),
    )
    msg1 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    msg2 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv.id,
        role=str(uuid7()),
        content=str(uuid7()),
    )

    m1 = mocker.patch(
        "prontia.db.cosmosdb.get_conversation",
        return_value=conv,
    )
    m2 = mocker.patch(
        "prontia.db.cosmosdb.delete_conversation",
    )
    m3 = mocker.patch(
        "prontia.db.cosmosdb.get_messages",
        return_value=[msg1, msg2],
    )
    m4 = mocker.patch(
        "prontia.db.cosmosdb.delete_message",
    )

    await target.delete_conversation(
        owner_id=TEST_OWNER_ID,
        id=conv.id,
    )

    assert m1.call_count == 1
    m1.assert_called_with(
        id=conv.id,
        owner_id=TEST_OWNER_ID,
    )
    assert m2.call_count == 1
    _, m2_kwargs = m2.call_args
    assert m2_kwargs["conversation"].id == conv.id
    assert m2_kwargs["conversation"].owner_id == conv.owner_id
    assert m3.call_count == 1
    _, m3_kwargs = m3.call_args
    assert m3_kwargs["owner_id"] == TEST_OWNER_ID
    assert m3_kwargs["conversation_id"] == conv.id
    assert m4.call_count == 2
    m4_args = m4.call_args_list
    _, m4_kwargs = m4_args[0]
    assert m4_kwargs["message"].id == msg1.id
    assert m4_kwargs["message"].owner_id == msg1.owner_id
    assert m4_kwargs["message"].conversation_id == msg1.conversation_id
    _, m4_kwargs = m4_args[1]
    assert m4_kwargs["message"].id == msg2.id
    assert m4_kwargs["message"].owner_id == msg2.owner_id
    assert m4_kwargs["message"].conversation_id == msg2.conversation_id


@pytest.mark.asyncio
async def test_delete_conversation_2(
    mocker: Mocker,
) -> None:
    mocker.patch(
        "prontia.db.cosmosdb.get_conversation",
        return_value=None,
    )

    with pytest.raises(ValueError):
        await target.get_conversation(
            id=str(uuid7()),
            owner_id=TEST_OWNER_ID,
        )


@pytest.mark.asyncio
async def test_get_conversation_messages_1(
    mocker: Mocker,
) -> None:
    conv_id = str(uuid7())
    msg1 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    msg2 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    m = mocker.patch(
        "prontia.db.cosmosdb.get_messages",
        return_value=[msg1, msg2],
    )

    msgs = await target.get_conversation_messages(
        owner_id=TEST_OWNER_ID,
        id=conv_id,
    )

    assert m.call_count == 1
    m.assert_called_with(
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
    )

    assert len(msgs) == 2
    assert msgs[0].id == msg1.id
    assert msgs[0].owner_id == msg1.owner_id
    assert msgs[0].conversation_id == msg1.conversation_id
    assert msgs[0].role == msg1.role
    assert msgs[0].content == msg1.content
    assert msgs[1].id == msg2.id
    assert msgs[1].owner_id == msg2.owner_id
    assert msgs[1].conversation_id == msg2.conversation_id
    assert msgs[1].role == msg2.role
    assert msgs[1].content == msg2.content


@pytest.mark.asyncio
async def test_completion_messages_1(
    mocker: Mocker,
) -> None:
    conv_id = str(uuid7())
    msg1 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    msg2 = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
        role=str(uuid7()),
        content=str(uuid7()),
    )
    content = str(uuid7())
    res_msg = Message(
        id=str(uuid7()),
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
        role=str(uuid7()),
        content=content,
    )

    m1 = mocker.patch(
        "prontia.db.cosmosdb.get_messages",
        return_value=[msg1, msg2],
    )
    m2 = mocker.patch(
        "prontia.services.openai.completion",
        return_value=res_msg,
    )
    m3 = mocker.patch(
        "prontia.db.cosmosdb.upsert_message",
        return_value=res_msg,
    )

    req, res = await target.completion_message(
        owner_id=TEST_OWNER_ID,
        id=conv_id,
        content=content,
    )

    assert m1.call_count == 1
    m1.assert_called_with(
        owner_id=TEST_OWNER_ID,
        conversation_id=conv_id,
    )
    assert m2.call_count == 1
    _, m2_kwargs = m2.call_args
    assert m2_kwargs["owner_id"] == TEST_OWNER_ID
    assert m2_kwargs["conversation_id"] != ""
    assert m2_kwargs["messages"].owner_id == TEST_OWNER_ID
    assert m2_kwargs["messages"].conversation_id == conv_id
    assert m2_kwargs["messages"].role == "user"
    assert m2_kwargs["messages"].content == content
    assert m2_kwargs["history"][0].id == msg1.id
    assert m2_kwargs["history"][0].owner_id == TEST_OWNER_ID
    assert m2_kwargs["history"][0].conversation_id == conv_id
    assert m2_kwargs["history"][0].role == msg1.role
    assert m2_kwargs["history"][0].content == msg1.content
    assert m2_kwargs["history"][1].id == msg2.id
    assert m2_kwargs["history"][1].owner_id == msg2.owner_id
    assert m2_kwargs["history"][1].conversation_id == conv_id
    assert m2_kwargs["history"][1].role == msg2.role
    assert m2_kwargs["history"][1].content == msg2.content
    assert m3.call_count == 1
    _, m3_kwargs = m3.call_args
    assert m3_kwargs["message"].id == res_msg.id
    assert m3_kwargs["message"].owner_id == TEST_OWNER_ID
    assert m3_kwargs["message"].conversation_id == conv_id
    assert m3_kwargs["message"].role == res_msg.role
    assert m3_kwargs["message"].content == res_msg.content

    assert res.id == res_msg.id
    assert res.owner_id == TEST_OWNER_ID
    assert res.conversation_id == conv_id
    assert res.role == res_msg.role
    assert res.content == res_msg.content

    assert req.id != res_msg.id
    assert req.owner_id == TEST_OWNER_ID
    assert req.conversation_id == conv_id
    assert req.role == "user"
    assert req.content == content