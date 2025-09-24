# backend/routers/worker.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import schemas, crud, models
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

@router.post("/pickups/confirm/{pickup_id}")
async def confirm_pickup(
    pickup_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(worker_access)
):
    pickup = await crud.get_pickup_by_id(db, pickup_id)
    if not pickup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pickup not found")
    if pickup.worker_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to confirm this pickup")
    if pickup.status == models.PickupStatus.collected:
        return pickup
    updated = await crud.update_pickup_status(db, pickup_id=pickup_id, new_status=models.PickupStatus.collected)
    return updated