def test_student_lifecycle(client):
    # --- STEP 1: CREATE ---
    response = client.post(
        "/students/",
        json={"name": "Test Student", "major": "Physics", "gpa": "3.5"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Student"
    assert "id" in data
    student_id = data["id"]

    # --- STEP 2: READ ALL ---
    response = client.get("/students/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == student_id

    # --- STEP 3: READ ONE ---
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["major"] == "Physics"

    # --- STEP 4: UPDATE ---
    # Change major to Math
    response = client.put(
        f"/students/{student_id}",
        json={"major": "Math"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["major"] == "Math"
    assert data["name"] == "Test Student" # Should stay the same

    # Verify update persisted
    response = client.get(f"/students/{student_id}")
    assert response.json()["major"] == "Math"

    # --- STEP 5: DELETE ---
    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 200
    assert response.json()["id"] == student_id

    # --- STEP 6: VERIFY DELETION ---
    response = client.get(f"/students/{student_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

def test_create_student_validation(client):
    # Test missing required field (major)
    response = client.post(
        "/students/",
        json={"name": "Bad Request Student"}
    )
    assert response.status_code == 422 # Unprocessable Entity