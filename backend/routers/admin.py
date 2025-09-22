# backend/routers/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Corrected: Changed relative imports
import schemas, crud
from database import get_db
from dependencies import role_checker

router = APIRouter()
# ... (rest of the file is the same)