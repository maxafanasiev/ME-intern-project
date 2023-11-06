from fastapi.security import HTTPAuthorizationCredentials

refresh_token = None
access_token = None


def test_signin(test_client):
    request_body = {
        "username": "1@1.com",
        "password": "testtest"
    }
    response = test_client.post("/auth/signin", data=request_body)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["refresh_token"]
    assert response.json()["token_type"]
    global refresh_token, access_token
    refresh_token = response.json()["refresh_token"]
    access_token = response.json()["access_token"]


def test_refresh_token(authorized_client):
    response = authorized_client.get("/auth/refresh_token", headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["refresh_token"]
    assert response.json()["token_type"]


def test_get_current_user(authorized_client):
    response = authorized_client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["id"]
