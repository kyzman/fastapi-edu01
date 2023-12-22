from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app import schemas

# SECRET_KEY
# Algorithm
# Expiration time

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d225e094faa6c5a437a256c81c8f67b7a9563eb93f7406f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = payload.get("user_id")

        if uid is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=uid)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
