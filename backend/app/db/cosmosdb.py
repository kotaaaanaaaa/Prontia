from azure.cosmos import PartitionKey
from azure.cosmos.aio import CosmosClient, DatabaseProxy, ContainerProxy
from datetime import datetime
from typing import List, Dict

from app.core.logging import log
from app.core.settings import settings
from app.models.data import Conversation, Message


__SELECT_QUERY = \
    'select * from c '\
    'where c.user_id = @user_id '


__CONVERSATION_SELECT_QUERY = \
    __SELECT_QUERY +\
    'and c.type = "conversation" '


__MESSAGE_SELECT_QUERY = \
    __SELECT_QUERY +\
    'and c.type = "message" '\
    'and c.conversation_id = @conversation_id '


async def __get_client() -> CosmosClient:
    '''

    '''
    client = CosmosClient(
        url=settings.cosmosdb.ENDPOINT,
        credential=settings.cosmosdb.ACCOUNTKEY,
    )
    await client.__aenter__()

    return client


async def __close_client(
        client: CosmosClient
) -> None:
    '''

    '''
    await client.close()


async def __get_database(
        client: CosmosClient,
) -> DatabaseProxy:
    '''

    '''
    database = await client.create_database_if_not_exists(
        id=settings.cosmosdb.DATABASE,
    )
    return database


async def __get_container(
        client: CosmosClient,
        container_name: str,
) -> ContainerProxy:
    '''

    '''
    database = await __get_database(client=client)
    container = await database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/user_id"),
    )
    return container


async def __query_container(
        container_name: str,
        query: str,
        parameters: List[Dict[str, object]] | None = None,
):
    try:
        client = await __get_client()
        container = await __get_container(
            client=client,
            container_name=container_name
        )
        result = container.query_items(
            query=query,
            parameters=parameters,
        )
        items = [item async for item in result]
        await __close_client(client=client)
        return items
    except Exception:
        log.exception('Error querying container')
        raise


async def __query_conversations(
        query: str,
        parameters: List[Dict[str, object]] | None = None,
):
    items = await __query_container(
        container_name='conversations',
        query=query,
        parameters=parameters,
    )
    return items


async def upsert_conversation(
        conversation: Conversation,
) -> Conversation:
    '''

    '''
    try:
        client = await __get_client()
        container = await __get_container(
            client=client,
            container_name='conversations'
        )

        now = datetime.now()
        if conversation.created_at is None:
            conversation.created_at = now
        conversation.updated_at = now
        item = conversation.model_dump(mode='json')

        await container.upsert_item(item)
        await __close_client(client=client)
        return conversation
    except Exception:
        log.exception('Error upserting conversation')
        raise


async def get_conversations(
        user_id: str,
) -> List[Conversation]:
    '''

    '''
    query = __CONVERSATION_SELECT_QUERY
    items = await __query_conversations(
        query=query,
        parameters=[
            dict(name='@user_id', value=user_id),
        ]
    )
    convs = [Conversation.model_validate(item) for item in items]

    return convs


async def get_conversation(
        user_id: str,
        id: str,
) -> Conversation:
    '''

    '''
    query = __CONVERSATION_SELECT_QUERY +\
        'and c.conversation_id = @conversation_id '
    items = await __query_conversations(
        query=query,
        parameters=[
            dict(name='@user_id', value=user_id),
            dict(name='@conversation_id', value=id),
        ]
    )
    convs = [Conversation.model_validate(item) for item in items]

    return convs[0]


async def delete_conversation(
        user_id: str,
        conversation_id: str,
) -> None:
    '''

    '''
    try:
        client = await __get_client()
        container = await __get_container(
            client=client,
            container_name='conversations'
        )
        await container.delete_item(
            item=conversation_id,
            partition_key=user_id,
        )
        await __close_client(client=client)
    except Exception:
        log.exception('Error deleting conversation')
        raise


async def upsert_message(
        message: Message,
) -> None:
    '''

    '''
    try:
        client = await __get_client()
        container = await __get_container(
            client=client,
            container_name='conversations'
        )

        now = datetime.now()
        if message.created_at is None:
            message.created_at = now
        message.updated_at = now
        item = message.model_dump(mode='json')

        await container.upsert_item(body=item)
        await __close_client(client=client)
        return message
    except Exception:
        log.exception('Error upserting message')
        raise


async def get_messages(
        user_id: str,
        conversation_id: str,
) -> List[Message]:
    '''

    '''
    query = __MESSAGE_SELECT_QUERY
    items = await __query_conversations(
        query=query,
        parameters=[
            dict(name='@user_id', value=user_id),
            dict(name='@conversation_id', value=conversation_id),
        ]
    )
    msgs = [Message.model_validate(item) for item in items]

    return msgs


async def get_message(
        user_id: str,
        conversation_id: str,
        id: str
) -> Message:
    '''

    '''
    query = __MESSAGE_SELECT_QUERY +\
        'and c.message_id = @messageId '
    items = await __query_conversations(
        query=query,
        parameters=[
            dict(name='@userId', value=user_id),
            dict(name='@conversationId', value=conversation_id),
            dict(name='@messageId', value=id),
        ]
    )
    msgs = [Message.model_validate(item) for item in items]

    return msgs[0]


async def delete_message(
        message: Message,
) -> None:
    '''

    '''
    try:
        client = await __get_client()
        container = await __get_container(
            client=client,
            container_name='conversations'
        )
        await container.delete_item(
            item=message.id,
            partition_key=message.user_id,
        )
        await __close_client(client=client)
    except Exception:
        log.exception('Error deleting message')
        raise


async def delete_messages(
        user_id: str,
        conversation_id: str,
) -> None:
    raise NotImplementedError()
