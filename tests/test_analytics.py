def test_user_global_analytics(authorized_client):
    response = authorized_client.get("/analytics/user/global-score/14")
    assert response.status_code == 200


def test_list_of_average_scores_by_quizzes(authorized_client):
    response = authorized_client.get("/analytics/user/quizzes-score/self")
    assert response.status_code == 200


def test_quizzes_list_with_time_of_passing_analytics(authorized_client):
    response = authorized_client.get("/analytics/user/quizzes-time-passing/self")
    assert response.status_code == 200


def test_users_scores_analytics_in_company(authorized_client):
    response = authorized_client.get("/analytics/admin/all-users-scores/3")
    assert response.status_code == 200


def test_get_user_average_scores_all_quizzes_in_company_over_time(authorized_client):
    response = authorized_client.get("/analytics/admin/user-scores-all-quizzes/3/14")
    assert response.status_code == 200


def test_get_users_last_completion_time_in_company(authorized_client):
    response = authorized_client.get("/analytics/admin/users-last-completion-time/3")
    assert response.status_code == 200
