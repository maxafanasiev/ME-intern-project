question_id = None


def test_create_question(authorized_client):
    request_body = {
        "question_text": "question1",
        "question_answers": [
            "1",
            "2",
            "3"
        ],
        "question_correct_answers": "2"
    }
    response = authorized_client.post("/questions/add-question-to-quiz/10", json=request_body)
    assert response.status_code == 201
    global question_id
    question_id = response.json()["id"]


def test_get_question_by_id(authorized_client):
    response = authorized_client.get(f"/questions/{question_id}")
    assert response.status_code == 200


def test_update_question(authorized_client):
    request_body = {
        "question_text": "question2",
        "question_answers": [
            "2",
            "4",
            "6"
        ],
        "question_correct_answers": "6"
    }
    response = authorized_client.put(f"/questions/{question_id}", json=request_body)
    assert response.status_code == 200


def test_delete_question(authorized_client):
    response = authorized_client.delete(f"/questions/{question_id}")
    assert response.status_code == 200


def test_get_question_in_quiz(authorized_client):
    response = authorized_client.get("/questions/all-in-quiz/10")
    assert response.status_code == 200
