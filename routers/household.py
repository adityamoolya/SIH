# backend/routers/household.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import schemas, crud
from database import get_db
from dependencies import role_checker

router = APIRouter()
household_access = role_checker(["household"])

@router.get("/waste-logs", response_model=List[schemas.WasteLog])
async def get_household_waste_logs(
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(household_access)
):
    return await crud.get_waste_logs_by_user(db, user_id=current_user.id)

@router.get("/rewards", response_model=List[schemas.Reward])
async def get_household_rewards(
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(household_access)
):
    return await crud.get_rewards_by_user(db, user_id=current_user.id)