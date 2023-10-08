join_request_id = None


def test_send_join_request(authorized_client):
    response = authorized_client.post("/user-actions/send-join-request/3")
    assert response.status_code == 201
    global join_request_id
    join_request_id = response.json()['id']
    assert "id" in response.json()


def test_reject_join_request(authorized_client):
    response = authorized_client.delete(f"/user-actions/reject-join-request/{join_request_id}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_invitations_to_user(authorized_client):
    response = authorized_client.get("/user-actions/invitations")
    assert response.status_code == 200
    assert "user_invitation" in response.json()


def test_get_all_user_join_requests(authorized_client):
    response = authorized_client.get("/user-actions/join-requests")
    assert response.status_code == 200
    assert "user_join_request" in response.json()


def test_user_reject_invitation(authorized_client):
    invitation = authorized_client.post("/company-actions/send-invitation/3/14")
    assert invitation.status_code == 201
    response = authorized_client.post(f"/user-actions/reject-invitation/{invitation.json()['id']}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_accept_invitation(authorized_client):
    invitation = authorized_client.post("/company-actions/send-invitation/3/14")
    assert invitation.status_code == 201
    response = authorized_client.post(f"/user-actions/accept-invitation/{invitation.json()['id']}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_leave_from_company(authorized_client):
    response = authorized_client.post("/user-actions/leave-from-company/3")
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_notification(authorized_client):
    response = authorized_client.get("/user-actions/notifications")
    assert response.status_code == 200
    assert "notifications" in response.json()


def test_mark_notification_as_read(authorized_client):
    notifications = authorized_client.get("/user-actions/notifications")
    not_read_notify_id = 999999
    n = notifications.json()['notifications']
    for notify in n:
        if notify["status"] == "unread":
            not_read_notify_id = notify['id']
            response = authorized_client.post(f"/user-actions/notifications/{not_read_notify_id}/read")
            assert response.status_code == 200
            assert "id" in response.json()
            break
    if not_read_notify_id == 999999:
        response = authorized_client.post("f/user-actions/notifications/{not_read_notify_id}/read")
        assert response.status_code == 404
