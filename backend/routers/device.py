# backend/routers/device.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Corrected: Changed relative imports
import sys
import os

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import schemas
from database import get_db

router = APIRouter()
# ... (rest of the file is the same)