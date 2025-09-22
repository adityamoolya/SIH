# backend/routers/worker.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import schemas, crud
from database import get_db
from dependencies import role_checker

router = APIRouter()
worker_access = role_checker(["worker"])

@router.get("/pickups", response_model=List[schemas.Pickup])
async def get_worker_pickups(
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(worker_access)
):
    return await crud.get_pickups_by_worker(db, worker_id=current_user.id)

@router.post("/confirm-pickup")
async def confirm_pickup(
    current_user: schemas.User = Depends(worker_access)
):
    return {"message": "Pickup confirmed successfully (placeholder)"}