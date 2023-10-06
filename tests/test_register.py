import requests
import os

base_url = 'http://127.0.0.1:8000'  # Replace with your actual URL
test_user_name = "bubu"
TOKEN = os.environ[f"{test_user_name.upper()}_TOKEN"]

def test_register_user():
    response = requests.post(
        f"{base_url}/register/",
        json={"username": test_user_name},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful"}

def test_register_existing_user():
    response = requests.post(
        f"{base_url}/register/",
        json={"username": test_user_name},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}
