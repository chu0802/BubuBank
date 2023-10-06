from datetime import datetime, timedelta
import os
from jose import jwt

SECRET_KEY = os.environ["PRIVITE_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*365

# Function to create a token
def create_token(username: str, expires_delta: timedelta):
    to_encode = {"sub": username, "exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Generate a token without a password
def generate_token(username: str):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(username, expires_delta)
    return access_token

if __name__ == '__main__':
    name = input("Type your username: ")
    token = generate_token(name)
    with open('.token.sh', "a+") as f:
        f.write(f"export {name.upper()}_TOKEN={token}\n")