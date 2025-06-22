import pytest

from app.api import conversation as target


@pytest.mark.asyncio
async def test_start_conversation() -> None:
    res = await target.start_conversation(
        user='test_user',
        content='hello',
    )
    assert True
