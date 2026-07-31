from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_the_email():
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    unregister_response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )
    activities_response = client.get("/activities")
    activity = activities_response.json()[activity_name]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_error():
    # Arrange
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants/{email}"
    )

    # Assert
    assert response.status_code == 400
    assert "Participant not found" in response.json()["detail"]
