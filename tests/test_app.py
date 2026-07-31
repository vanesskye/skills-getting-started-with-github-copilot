from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_the_email():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    activity = activities_response.json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_error():
    response = client.delete(
        "/activities/Chess Club/participants/missing.student@mergington.edu"
    )

    assert response.status_code == 400
    assert "Participant not found" in response.json()["detail"]
