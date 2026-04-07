from src import app as app_module


def test_root_redirects_to_static_index(test_client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = test_client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(test_client):
    # Arrange

    # Act
    response = test_client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert "Chess Club" in json_data
    assert json_data["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_student(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "test.student@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_missing_activity_returns_404(test_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "new.student@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_student(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_missing_student_returns_400(test_client):
    # Arrange
    activity_name = "Chess Club"
    email = "unknown@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_missing_activity_returns_404(test_client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test.student@mergington.edu"

    # Act
    response = test_client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
