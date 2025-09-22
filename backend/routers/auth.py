# backend/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from typing import Annotated

# Corrected: Changed relative imports
# import schemas, crud
from database import get_db
from auth_utils import authenticate_user, create_access_token

router = APIRouter(tags=["Authentication"])

# ... (rest of the file is the same)