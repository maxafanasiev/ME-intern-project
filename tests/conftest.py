import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
def authorized_client():
    client = TestClient(app)

    username = '1@1.com'
    password = 'testtest'

    response = client.post("/auth/signin", data={"username": username, "password": password})
    assert response.status_code == 200
    client.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    yield client
