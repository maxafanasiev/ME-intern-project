def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_db_heath(test_client):
    response = test_client.get("/db_health/")
    assert response.status_code == 200


def test_redis_heath(test_client):
    response = test_client.get("/redis_health/")
    assert response.status_code == 200


def test_password_hashing(test_client):
    password = fake.password(length=random.randint(8, 16))
    hashed_password = auth_service.get_password_hash(password)
    verify_password = auth_service.verify_password(password, hashed_password)
    assert verify_password is True

