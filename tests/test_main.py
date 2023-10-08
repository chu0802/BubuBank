import os

import requests

base_url = "http://127.0.0.1:8000"  # Replace with your actual URL
test_user_name = "test_user"
TOKEN = os.environ[f"{test_user_name.upper()}_TOKEN"]


def test_register_user():
    response = requests.post(
        f"{base_url}/register/",
        json={"username": test_user_name},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful"}


def test_register_existing_user():
    response = requests.post(
        f"{base_url}/register/",
        json={"username": test_user_name},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Username already exists"}


def test_balance():
    # Check initial balance (should be 0)
    response = requests.get(
        f"{base_url}/balance/", headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json() == {"balance": 0.0}


def test_deposit():
    # Deposit 100 units
    response = requests.post(
        f"{base_url}/deposit/",
        json={"amount": 100},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    # Check if deposit is successful
    assert response.status_code == 200
    assert response.json() == {"message": "Deposit successful", "balance": 100.0}


def test_withdraw():
    # Withdraw 50 units
    response = requests.post(
        f"{base_url}/withdraw/",
        json={"amount": 50},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    # Check if withdrawal is successful
    assert response.status_code == 200
    assert response.json() == {"message": "Withdrawal successful", "balance": 50.0}


def test_balance_after_modifying():
    # Check balance after withdrawal
    response = requests.get(
        f"{base_url}/balance/", headers={"Authorization": f"Bearer {TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json() == {"balance": 50.0}


def test_delete_user():
    # Delete user 'new_user'
    response = requests.delete(
        f"{base_url}/delete_user/{test_user_name}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    # Check if user was deleted successfully
    assert response.status_code == 200
    assert response.json() == {"message": f"User '{test_user_name}' has been deleted"}

    # Try to delete user 'new_user' again (should fail)
    response = requests.delete(
        f"{base_url}/delete_user/{test_user_name}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )

    # Check if deletion fails (user not found)
    assert response.status_code == 400
    assert response.json() == {"detail": f"User '{test_user_name}' not found"}

    # Try to delete user 'test_user' with incorrect token (should fail)
    response = requests.delete(
        f"{base_url}/delete_user/test_user",
        headers={"Authorization": f"Bearer incorrect_token"},
    )

    # Check if deletion fails (unauthorized)
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
