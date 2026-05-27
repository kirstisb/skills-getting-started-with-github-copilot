def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success_adds_participant(client):
    email = "new.student@mergington.edu"

    signup_response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert signup_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_fails_for_unknown_activity(client):
    response = client.post("/activities/NotARealClub/signup", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_fails_for_duplicate_participant(client):
    existing_email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_success_removes_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.delete("/activities/Chess Club/participants", params={"email": existing_email})
    assert response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert existing_email not in participants


def test_unregister_fails_for_unknown_activity(client):
    response = client.delete("/activities/NotARealClub/participants", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_fails_for_missing_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants", params={"email": "not-enrolled@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"