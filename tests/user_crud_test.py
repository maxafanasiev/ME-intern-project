import random

from faker import Faker

fake = Faker()

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


def test_sign_up(test_client):
    response = test_client.post("/users/signup", json=signup_data)

    assert response.status_code == 201

    user_data = response.json()
    assert "user_id" in user_data
    assert "user_email" in user_data
    assert "user_firstname" in user_data
    assert "user_lastname" in user_data

    signup_data.update({"user_id": user_data["user_id"]})


def test_get_user(test_client):
    # user_id = signup_data["user_id"]
    user_id = 20
    print(user_id)
    response = test_client.get(f"/users/{user_id}")

    assert response.status_code == 200

    user_data = response.json()
    assert "user_id" in user_data
    assert "user_email" in user_data
    assert "user_firstname" in user_data
    assert "user_lastname" in user_data


def test_update_user(test_client):
    user_id = signup_data["user_id"]
    upgrade_data = {
        "user_firstname": fake.first_name()[:50],
        "user_lastname": fake.last_name()[:50],
    }
    response = test_client.put(f"/users/{user_id}", json=upgrade_data)

    assert response.status_code == 200


def test_get_users(test_client):
    response = test_client.get("/users/")

    assert response.status_code == 200
    user_list = response.json().get("users")
    assert user_list is not None
    assert len(user_list) > 0


def test_delete_user(test_client):
    user_id = signup_data["user_id"]
    response = test_client.delete(f"/users/{user_id}")

    assert response.status_code == 200
