from faker import Faker

fake = Faker()
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im1heG9sb2xvbG9AZ21haWwuY29tIiwiZmlyc3RfbmFtZSI6Ik1heCIsImxhc3RfbmFtZSI6IkFmYW5hc3lldiIsImlzcyI6Imh0dHBzOi8vbWVkLWludGVybnNoaXAuZXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1ODEyMzA5NzMxMzEzMDIwNTE2IiwiYXVkIjpbImh0dHA6Ly8wLjAuMC4wOjgwMDAvIl0sImlhdCI6MTY5NTkzMzAxNywiZXhwIjoxNjk2MDE5NDE3LCJhenAiOiJGYWE5VURJY0lDQmtmcW43MGxSZ1U4RldmV294SlJIaCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.01Fz8H_lWCWhNaEHweAxbacZh9AuQk1ohg0I0ffI2hk"

create_data = {
    "company_name": fake.company()[:50],
    "company_title": fake.text()[:30],
    "company_description": fake.text(),
    "company_city": fake.city()[:50],
    "company_phone": fake.phone_number()[:15],
    "company_links": [fake.url()[:50]],
    "company_avatar": fake.image_url()[:50],
    "is_visible": "True"
}


def test_create_company(test_client):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/companies/", json=create_data, headers=headers)

    assert response.status_code == 201

    company_data = response.json()
    assert "id" in company_data

    create_data.update({"id": company_data["id"]})


def test_create_company_unautorize(test_client):
    response = test_client.post("/companies/", json=create_data)

    assert response.status_code == 401


def test_get_company(test_client):
    company_id = create_data["id"]
    response = test_client.get(f"/companies/{company_id}")

    assert response.status_code == 200


def test_get_company_not_found(test_client):
    company_id = 99999
    response = test_client.get(f"/companies/{company_id}")

    assert response.status_code == 404


def test_update_company(test_client):
    company_id = create_data["id"]
    upgrade_data = {
        "company_city": fake.city()[:50],
        "company_phone": fake.phone_number()[:15]
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.put(f"/companies/{company_id}", headers=headers, json=upgrade_data)

    assert response.status_code == 200


def test_update_user_not_authorisation(test_client):
    company_id = create_data["id"]
    upgrade_data = {
        "company_city": fake.city()[:50],
        "company_phone": fake.phone_number()[:15]
    }
    response = test_client.put(f"/companies/{company_id}", json=upgrade_data)

    assert response.status_code == 401


def test_get_companies(test_client):
    response = test_client.get("/companies/")

    assert response.status_code == 200
    companies_list = response.json().get("companies")
    assert companies_list is not None
    assert len(companies_list) > 0


def test_delete_company_not_authorisation(test_client):
    company_id = create_data["id"]
    response = test_client.delete(f"/companies/{company_id}")

    assert response.status_code == 401


def test_delete_company(test_client):
    company_id = create_data["id"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.delete(f"/companies/{company_id}", headers=headers)

    assert response.status_code == 200
