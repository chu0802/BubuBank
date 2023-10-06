from fastapi import FastAPI, HTTPException, Depends, Security, Header
from pydantic import BaseModel
from jose import JWTError, jwt

import sqlite3
import os

app = FastAPI()

# Create a connection and a cursor for SQLite
conn = sqlite3.connect('balances.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        balance REAL
    )
''')
conn.commit()

SECRET_KEY = os.environ["PRIVITE_KEY"]
ALGORITHM = "HS256"

class Transaction(BaseModel):
    amount: float

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequest(BaseModel):
    username: str



# Function to decode a token
def decode_token(token: str):
    try:
        token = token.split()[-1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except JWTError as e:
        print(f"Error decoding token: {e}")
        return None

def get_current_user(token: str):
    username = decode_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

@app.post("/deposit/")
async def deposit(
    transaction: Transaction,
    authorization: str = Header(None)
):
    current_user = get_current_user(authorization)
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE username = ?", (transaction.amount, current_user))
    conn.commit()
    return {"message": "Deposit successful", "balance": read_balance(current_user)}

@app.post("/withdraw/")
async def withdraw(
    transaction: Transaction,
    authorization: str = Header(None)
):
    current_user = get_current_user(authorization)
    cursor.execute("SELECT balance FROM accounts WHERE username = ?", (current_user,))
    current_balance = cursor.fetchone()[0]
    if current_balance >= transaction.amount:
        cursor.execute("UPDATE accounts SET balance = balance - ? WHERE username = ?", (transaction.amount, current_user))
        conn.commit()
        return {"message": "Withdrawal successful", "balance": read_balance(current_user)}
    else:
        raise HTTPException(status_code=400, detail="Insufficient funds")

@app.get("/balance/")
async def show_balance(authorization: str = Header(None)):
    current_user = get_current_user(authorization)
    return {"balance": read_balance(current_user)}

def read_balance(username):
    cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
    balance = cursor.fetchone()[0]
    return balance

@app.post("/register/", response_model=dict)
async def register(authorization: str = Header(None)):
    current_user = get_current_user(authorization)
    # Check if the username already exists
    cursor.execute("SELECT COUNT(*) FROM accounts WHERE username = ?", (current_user,))
    count = cursor.fetchone()[0]
    if count > 0:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Insert the new user with balance 0
    cursor.execute("INSERT INTO accounts (username, balance) VALUES (?, ?)", (current_user, 0))
    conn.commit()
    
    return {"message": "Registration successful"}


@app.delete("/delete_user/{username}")
async def delete_user(username: str, authorization: str = Header(None)):
    current_user = get_current_user(authorization)
    if current_user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if current_user != username:
        raise HTTPException(status_code=401, detail="You can only delete your own account")
    
    cursor.execute("SELECT COUNT(*) FROM accounts WHERE username = ?", (username,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        raise HTTPException(status_code=400, detail=f"User '{username}' not found")
    
    cursor.execute("DELETE FROM accounts WHERE username = ?", (username,))
    conn.commit()
    return {"message": f"User '{username}' has been deleted"}