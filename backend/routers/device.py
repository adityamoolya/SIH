# backend/routers/device.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import schemas, models, crud
from database import get_db

router = APIRouter()

@router.post("/upload")
async def upload_from_device(
    log: schemas.WasteLogCreate,
    db: AsyncSession = Depends(get_db)
):
    # Step 1: Find Household by device_id
    device_result = await db.execute(
        select(models.Device).filter(models.Device.device_id == log.device_id)
    )
    device = device_result.scalars().first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

    user_result = await db.execute(
        select(models.User).filter(models.User.id == device.user_id)
    )
    user = user_result.scalars().first()
    if not user or user.role != models.UserRole.household:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device not linked to a household user")

    # Step 2: Calculate points
    points = int(round(log.weight * 20))

    # Step 3: Create Waste Log
    await crud.create_waste_log(
        db,
        user_id=user.id,
        waste_type=log.waste_type,
        weight=log.weight,
        points=points,
        timestamp=log.timestamp,
    )

    # Step 4: Update Reward
    await crud.update_or_create_reward(db, user_id=user.id, points_to_add=points)

    # Step 5: Create Pickup for first worker (placeholder logic)
    worker_result = await db.execute(
        select(models.User).filter(models.User.role == models.UserRole.worker)
    )
    worker = worker_result.scalars().first()
    if worker:
        await crud.create_pickup(db, household_id=user.id, worker_id=worker.id)

    return {"message": "Waste log processed, reward updated, and pickup created"}