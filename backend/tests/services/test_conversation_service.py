import pytest

from app.services import conversation as target


@pytest.mark.asyncio
async def test_get_messages() -> None:
    res = await target.get_messages(
        user_id='test_user',
        conversation_id='01979024-d7b0-7c68-9d32-4ac66d0dd1fb',
    )
    assert res.count() > 0
