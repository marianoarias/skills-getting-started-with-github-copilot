from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_unregister_participant_returns_404_when_student_is_not_signed_up():
    response = client.delete("/activities/Chess Club/unregister?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
