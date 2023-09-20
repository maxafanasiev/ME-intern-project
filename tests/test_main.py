import random

import pytest
from faker import Faker

from app.main import redis

fake = Faker()


def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_redis_connection(test_client, redis_connection=redis):
    assert await redis_connection.ping() is True
