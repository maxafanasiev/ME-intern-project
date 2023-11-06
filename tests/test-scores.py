def test_get_user_score_in_company(authorized_client):
    response = authorized_client.get("/scores/14/3")
    assert response.status_code == 200


def test_get_user_score_global(authorized_client):
    response = authorized_client.get("/scores/14")
    assert response.status_code == 200
