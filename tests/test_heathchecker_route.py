from faker import Faker

fake = Faker()


def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_db_heath(test_client):
    response = test_client.get("/db_health/")
    assert response.status_code == 200


def test_redis_heath(test_client):
    response = test_client.get("/redis_health/")
    assert response.status_code == 200
