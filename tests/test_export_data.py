def test_export_self_user_results_to_json(authorized_client):
    response = authorized_client.get("/export-data/self/json")
    assert response.status_code == 200


def test_export_self_user_results_to_csv(authorized_client):
    response = authorized_client.get("/export-data/self/csv")
    assert response.status_code == 200


def test_export_user_result_in_company_json(authorized_client):
    response = authorized_client.get("/export-data/14/3/json")
    assert response.status_code == 200


def test_export_user_result_in_company_csv(authorized_client):
    response = authorized_client.get("/export-data/14/3/csv")
    assert response.status_code == 200


def test_export_all_users_result_in_company_json(authorized_client):
    response = authorized_client.get("/export-data/company/json/3")
    assert response.status_code == 200


def test_export_all_users_result_in_company_csv(authorized_client):
    response = authorized_client.get("/export-data/company/csv/3")
    assert response.status_code == 200


def test_export_users_in_quiz_json(authorized_client):
    response = authorized_client.get("/export-data/quiz/json/4")
    assert response.status_code == 200


def test_export_users_in_quiz_csv(authorized_client):
    response = authorized_client.get("/export-data/quiz/csv/4")
    assert response.status_code == 200
