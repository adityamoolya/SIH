# backend/auth_utils.py

import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
import crud, schemas
from password_utils import verify_password

SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key_for_local_dev")
# --- THIS IS THE FIX ---
ALGORITHM = "HS256" # Corrected from "HS26"
# ---------------------
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# The tokenUrl must match the full path to your login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await crud.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user