import requests
import os

base_url = 'http://127.0.0.1:8000'  # Replace with your actual URL
test_user_name = "bubu"
TOKEN = os.environ[f"{test_user_name.upper()}_TOKEN"]
BALANCE = None

def test_balance():
    # Check initial balance (should be 0)
    response = requests.get(f"{base_url}/balance/", headers={"Authorization": f"Bearer {TOKEN}"})
    assert response.status_code == 200
    global BALANCE
    BALANCE = response.json()["balance"]

def test_deposit():
    # Deposit 100 units
    response = requests.post(
        f"{base_url}/deposit/",
        json={"amount": 100},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    
    # Check if deposit is successful
    assert response.status_code == 200
    assert response.json() == {"message": "Deposit successful", "balance": 100.0 + BALANCE}

def test_withdraw():
    # Withdraw 50 units
    response = requests.post(
        f"{base_url}/withdraw/",
        json={"amount": 100},
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    # Check if withdrawal is successful
    assert response.status_code == 200
    assert response.json() == {"message": "Withdrawal successful", "balance": BALANCE}
 
    
def test_balance_after_modifying():
    # Check balance after withdrawal
    response = requests.get(f"{base_url}/balance/", headers={"Authorization": f"Bearer {TOKEN}"})
    assert response.status_code == 200
    assert response.json() == {"balance": BALANCE}
