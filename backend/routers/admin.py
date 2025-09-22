# backend/routers/admin.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import schemas, crud
from database import get_db
from dependencies import role_checker

router = APIRouter()
admin_access = role_checker(["admin"])

@router.get("/analytics", response_model=schemas.AdminAnalytics)
async def get_admin_analytics(db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(admin_access)):
    total_waste = await crud.get_total_waste_collected(db)
    active_households = await crud.get_active_households_count(db)
    return {
        "total_waste_collected": total_waste,
        "segregation_accuracy": 95.5,
        "active_households": active_households,
    }

@router.get("/devices", response_model=List[schemas.Device])
async def get_all_devices(db: AsyncSession = Depends(get_db), current_user: schemas.User = Depends(admin_access)):
    return await crud.get_all_devices(db)