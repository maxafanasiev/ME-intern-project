quiz_id = None


def test_create_quiz(authorized_client):
    request_body = {
        "quiz_name": "TestQuiz",
        "quiz_title": "testtest",
        "quiz_description": "test description",
        "quiz_frequency": 3
    }
    response = authorized_client.post("/quizzes/3", json=request_body)
    assert response.status_code == 201
    global quiz_id
    quiz_id = response.json()["id"]


def test_get_quiz_by_id(authorized_client):
    response = authorized_client.get(f"/quizzes/quiz/{quiz_id}")
    assert response.status_code == 200


def test_update_quiz(authorized_client):
    request_body = {
        "quiz_name": "TestQuiz1",
        "quiz_title": "testtest2",
        "quiz_description": "test description2",
        "quiz_frequency": 2
    }
    response = authorized_client.put(f"/quizzes/{quiz_id}", json=request_body)
    assert response.status_code == 200


def test_delete_quiz(authorized_client):
    response = authorized_client.delete(f"/quizzes/{quiz_id}")
    assert response.status_code == 200


def test_get_quizzes_in_company(authorized_client):
    response = authorized_client.get("/quizzes/3")
    assert response.status_code == 200


def test_start_quiz(authorized_client):
    response = authorized_client.post("/quizzes/start/4")
    assert response.status_code == 200


def test_finish_quiz(authorized_client):
    request_body = {
        "answers": [
            {
                "question_id": 6,
                "answer": "string"
            },
            {
                "question_id": 7,
                "answer": "123"
            },
            {
                "question_id": 8,
                "answer": "string"
            }
        ]
    }
    response = authorized_client.post("/quizzes/submit/4", json=request_body)
    assert response.status_code == 200
