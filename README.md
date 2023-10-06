# BubuBank
This is a practice project featuring a RESTful API for managing financial transactions. This application allows users to record deposits, withdrawals, and check their account balance. It serves as a hands-on exercise in building and interacting with a RESTful API using FastAPI.

## Prerequisites

* Python 3.8+
* FastAPI
* SQLite

## Installing

* Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/fastapi-banking-api.git
```

* Install the required dependencies.

```bash
pip install -r requirements.txt
```

## Setup

Before starting the server, it's important to set up your private key for JWT validation.

1. Create a file named .env.sh in the project root.

2. Add the following content to .env.sh:


```bash
export PRIVITE_KEY=<YOUR_PRIVITE_KEY>
```

* Replace <YOUR_PRIVATE_KEY> with your actual private key.

This private key is essential for secure JWT token validation. Please ensure it remains confidential and is not shared publicly.

## Running the server application

Before startint the server, enable the environment variables.

```bash
source .env.sh
```

Then, start the FastAPI application.

```bash
uvicorn main:app --reload
```

## API Endpoints

### Register

* URL: `/register/`
* Method: `POST`
#### Request Header
```json
{
  "Authorization": "Bearer your_access_token"
}
```

#### Response
```json
{
  "message": "Registration successful"
}
```
---

### Delete User

* URL: `/delete_user/{username}`
* Method: `DELETE`

#### Request Header:

```json
{
  "Authorization": "Bearer your_access_token"
}
```

#### Response

```json
{
  "message": "User 'username' has been deleted"
}
```
---

### Deposit

* URL: `/deposit/`
* Method: `POST`

#### Request Body:

```json
{
  "amount": 100
}
```

#### Response

```json
{
  "message": "Deposit successful",
  "balance": 100
}
```
---

### Withdraw

* URL: `/withdraw/`
* Method: `POST`

#### Request Body:

```json
{
  "amount": 50
}
```

#### Response

```json
{
  "message": "Withdrawal successful",
  "balance": 50
}
```
---

### Check Balance
* URL: `/balance/`
* Method: `GET`

#### Response

```json
{
  "balance": 50
}
```

---

## Running Tests

* You can run the tests using pytest. Make sure the FastAPI application is running before running the tests.

* Before testing, you will need to first generate a valid token

### Generate token

```bash
python utils/generate_token.py
```

The program will guide you to enter a username, and automatically store the corresponding token to `.token.sh`

Then, before running the client side / test code, enable your token.

```bash
source .token.sh
```

---
### Register a new member

```bash
pytest tests/test_register.py
```
---
### Test deposit / withdraw with an existing member

```bash
pytest tests/test_deposit.py
```
---
### Test the whole procedure

```bash
pytest tests/test_main.py
```
---
