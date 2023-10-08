invitation_id = None


def test_send_invitation(authorized_client):
    response = authorized_client.post("/company-actions/send-invitation/3/14")
    assert response.status_code == 201
    assert "id" in response.json()
    global invitation_id
    invitation_id = response.json()["id"]


def test_reject_invitation(authorized_client):
    response = authorized_client.delete(f"/company-actions/reject-invitation/{invitation_id}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_all_invitations(authorized_client):
    response = authorized_client.get("/company-actions/invitations/3")
    assert response.status_code == 200
    assert "company_invitation" in response.json()


def test_get_all_join_requests(authorized_client):
    response = authorized_client.get("/company-actions/join-requests/3")
    assert response.status_code == 200
    assert "company_join_request" in response.json()


def test_reject_join_requests(authorized_client):
    join_request = authorized_client.post("/user-actions/send-join-request/3")
    assert join_request.status_code == 201
    response = authorized_client.post(f"/company-actions/reject-join-request/{join_request.json()['id']}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_accept_join_requests(authorized_client):
    join_request = authorized_client.post("/user-actions/send-join-request/3")
    assert join_request.status_code == 201
    response = authorized_client.post(f"/company-actions/accept-join-request/{join_request.json()['id']}")
    assert response.status_code == 200
    assert "id" in response.json()


def test_set_admin_in_company(authorized_client):
    response = authorized_client.post("/company-actions/set-admin/3/14")
    assert response.status_code == 200
    assert "id" in response.json()


def test_remove_admin_in_company(authorized_client):
    response = authorized_client.post("/company-actions/remove-admin/3/14")
    assert response.status_code == 200
    assert "id" in response.json()


def test_remove_user_from_company(authorized_client):
    response = authorized_client.post("/company-actions/remove-user-from-company/3/14")
    assert response.status_code == 200
    assert "id" in response.json()
