from datetime import datetime
from typing import List, Dict, Any

from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, DatabaseProxy, ContainerProxy
from pydantic_core import ValidationError

from prontia.core.logging import log
from prontia.core.settings import settings
from prontia.models.conversation import Conversation
from prontia.models.message import Message


async def _get_client() -> CosmosClient:
    client = CosmosClient(
        url=settings.cosmosdb.ENDPOINT,
        credential=settings.cosmosdb.ACCOUNTKEY,
    )
    await client.__aenter__()
    return client


async def _close_client(
    client: CosmosClient,
) -> None:
    await client.close()


async def _get_database(
    client: CosmosClient,
) -> DatabaseProxy:
    database = await client.create_database_if_not_exists(
        id=settings.cosmosdb.DATABASE,
    )
    return database


async def _get_container(
    client: CosmosClient,
    name: str,
    path: str,
) -> ContainerProxy:
    database = await _get_database(client=client)
    container = await database.create_container_if_not_exists(
        id=name,
        partition_key=PartitionKey(path=path),
    )
    return container


async def _upsert_item(
    container_name: str,
    partition_path: str,
    item: dict[str, Any],
) -> dict[str, Any]:
    try:
        client = await _get_client()
        container = await _get_container(
            client=client,
            name=container_name,
            path=partition_path,
        )

        result = await container.upsert_item(
            item,
        )
        await _close_client(client=client)
        return result
    except Exception:
        log.exception("Error upserting container {container_name}")
        raise


async def _delete_item(
    item_id: str,
    partition_key: str,
    container_name: str,
    partition_path: str,
) -> None:
    try:
        client = await _get_client()
        container = await _get_container(
            client=client,
            name=container_name,
            path=partition_path,
        )
        await container.delete_item(
            item=item_id,
            partition_key=partition_key,
        )
        await _close_client(client=client)
    except Exception:
        log.exception("Error deleting item container {container_name}")
        raise


async def _query_container(
    name: str,
    path: str,
    query: str,
    parameters: List[Dict[str, object]] | None = None,
) -> List[Dict[str, Any]]:
    try:
        client = await _get_client()
        container = await _get_container(
            client=client,
            name=name,
            path=path,
        )
        result = container.query_items(
            query=query,
            parameters=parameters,
        )
        items = [item async for item in result]
        await _close_client(client=client)
        return items
    except Exception:
        log.exception(f"Error querying container {name}")
        raise


_CONVERSATION_CONTAINER_NAME = "conversations"
_CONVERSATION_PARTITION_PATH = "/owner_id"
_CONVERSATION_SELECT_QUERY = (
    "select * from c where c.owner_id = @owner_id and c.type = 'conversation'"
)


async def query_conversations(
    query: str,
    parameters: List[Dict[str, object]] | None = None,
) -> List[Conversation]:
    items = await _query_container(
        name=_CONVERSATION_CONTAINER_NAME,
        path=_CONVERSATION_PARTITION_PATH,
        query=query,
        parameters=parameters,
    )
    convs = [Conversation.model_validate(item) for item in items]
    return convs


async def upsert_conversation(
    conversation: Conversation,
) -> Conversation:
    now = datetime.now()
    if conversation.created_at is None:
        conversation.created_at = now
    conversation.updated_at = now
    item = conversation.model_dump(mode="json")
    item["type"] = "conversation"

    res = await _upsert_item(
        container_name=_CONVERSATION_CONTAINER_NAME,
        partition_path=_CONVERSATION_PARTITION_PATH,
        item=item,
    )
    return Conversation.model_validate(res)


async def get_conversations(
    owner_id: str,
) -> List[Conversation]:
    query = _CONVERSATION_SELECT_QUERY
    items = await query_conversations(
        query=query,
        parameters=[
            dict(name="@owner_id", value=owner_id),
        ],
    )
    convs = [Conversation.model_validate(item) for item in items]
    return convs


async def get_conversation(
    id: str,
    owner_id: str,
) -> Conversation | None:
    query = _CONVERSATION_SELECT_QUERY + " and c.id = @conversation_id"
    items = await query_conversations(
        query=query,
        parameters=[
            dict(name="@owner_id", value=owner_id),
            dict(name="@conversation_id", value=id),
        ],
    )
    try:
        convs = [Conversation.model_validate(item) for item in items]
    except ValidationError as e:
        log.error(f"Validation error while getting conversation: {e.json()}")
    if len(convs) > 1:
        raise ValueError("Multiple conversations found with the same ID")
    if len(convs) == 0:
        return None
    return convs[0]


async def delete_conversation(
    conv: Conversation,
) -> None:
    await _delete_item(
        item_id=conv.id,
        partition_key=conv.owner_id,
        container_name=_CONVERSATION_CONTAINER_NAME,
        partition_path=_CONVERSATION_PARTITION_PATH,
    )


_MESSAGE_CONTAINER_NAME = "conversations"
_MESSAGE_PARTITION_PATH = "/owner_id"
_MESSAGE_SELECT_QUERY = 'select * from c where c.owner_id = @owner_id and c.type = "message" and c.conversation_id = @conversation_id'


async def query_messages(
    query: str,
    parameters: List[Dict[str, object]] | None = None,
) -> List[Message]:
    items = await _query_container(
        name=_MESSAGE_CONTAINER_NAME,
        path=_MESSAGE_PARTITION_PATH,
        query=query,
        parameters=parameters,
    )
    msgs = [Message.model_validate(item) for item in items]
    return msgs


async def upsert_message(
    message: Message,
) -> Message:
    now = datetime.now()
    if message.created_at is None:
        message.created_at = now
    message.updated_at = now
    item = message.model_dump(mode="json")
    item["type"] = "message"

    res = await _upsert_item(
        container_name=_MESSAGE_CONTAINER_NAME,
        partition_path=_MESSAGE_PARTITION_PATH,
        item=item,
    )
    return Message.model_validate(res)


async def get_messages(
    owner_id: str,
    conversation_id: str,
) -> List[Message]:
    query = _MESSAGE_SELECT_QUERY
    items = await query_messages(
        query=query,
        parameters=[
            dict(name="@owner_id", value=owner_id),
            dict(name="@conversation_id", value=conversation_id),
        ],
    )
    msgs = [Message.model_validate(item) for item in items]
    return msgs


async def get_message(
    id: str,
    owner_id: str,
    conversation_id: str,
) -> Message | None:
    query = _MESSAGE_SELECT_QUERY + " and c.id = @message_id"
    items = await query_messages(
        query=query,
        parameters=[
            dict(name="@owner_id", value=owner_id),
            dict(name="@conversation_id", value=conversation_id),
            dict(name="@message_id", value=id),
        ],
    )
    try:
        msgs = [Message.model_validate(item) for item in items]
    except ValidationError as e:
        log.error(f"Validation error while getting message: {e.json()}")
    if len(msgs) > 1:
        raise ValueError("Multiple messages found with the same ID")
    if len(msgs) == 0:
        return None
    return msgs[0]


async def delete_message(
    message: Message,
) -> None:
    await _delete_item(
        item_id=message.id,
        partition_key=message.owner_id,
        container_name=_MESSAGE_CONTAINER_NAME,
        partition_path=_MESSAGE_PARTITION_PATH,
    )
