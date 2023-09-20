import random

import pytest
from faker import Faker

from app.main import redis

fake = Faker()


def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_sign_up(test_client):
    signup_data = {
        "user_email": fake.email(),
        "user_firstname": fake.first_name()[:50],
        "user_lastname": fake.last_name()[:50],
        "user_status": random.choice(["Active", "Inactive", "Pending"])[:50],
        "user_city": fake.city()[:50],
        "user_phone": fake.phone_number()[:15],
        "user_links": [fake.url()[:50]],
        "user_avatar": fake.image_url()[:50],
        "password": fake.password(length=random.randint(8, 16)),
    }

    response = test_client.post("/users/signup", json=signup_data)

    assert response.status_code == 201

    user_data = response.json()
    assert "user_email" in user_data
    assert "user_firstname" in user_data
    assert "user_lastname" in user_data
    assert "user_status" in user_data
    assert "user_city" in user_data
    assert "user_phone" in user_data
    assert "user_links" in user_data
    assert "user_avatar" in user_data
    assert "password" in user_data


def test_password_hashing(test_client):
    password = fake.password(length=random.randint(8, 16))
    hashed_password = auth_service.get_password_hash(password)
    verify_password = auth_service.verify_password(password, hashed_password)
    assert verify_password is True


@pytest.mark.asyncio
async def test_redis_connection(test_client, redis_connection=redis):
    assert await redis_connection.ping() is True
