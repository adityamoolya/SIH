# backend/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional
from datetime import datetime
import models, schemas
from password_utils import get_password_hash

# --- User CRUD ---
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        role=user.role,
        password_hash=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- WasteLog CRUD ---
async def get_waste_logs_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.WasteLog).filter(models.WasteLog.user_id == user_id))
    return result.scalars().all()

# --- Reward CRUD ---
async def get_rewards_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Reward).filter(models.Reward.user_id == user_id))
    return result.scalars().all()

# --- Pickup CRUD ---
async def get_pickups_by_worker(db: AsyncSession, worker_id: int):
    result = await db.execute(select(models.Pickup).filter(models.Pickup.worker_id == worker_id))
    return result.scalars().all()

async def get_pickup_by_id(db: AsyncSession, pickup_id: int):
    result = await db.execute(select(models.Pickup).filter(models.Pickup.id == pickup_id))
    return result.scalars().first()

# --- Admin CRUD ---
async def get_total_waste_collected(db: AsyncSession):
    result = await db.execute(select(func.sum(models.WasteLog.weight)))
    return result.scalar_one_or_none() or 0.0

async def get_active_households_count(db: AsyncSession):
    result = await db.execute(select(func.count(models.User.id)).filter(models.User.role == 'household'))
    return result.scalar_one()

# --- Device CRUD ---
async def get_all_devices(db: AsyncSession):
    result = await db.execute(select(models.Device))
    return result.scalars().all()

# --- New Business Logic Helpers ---
async def create_waste_log(
    db: AsyncSession,
    *,
    user_id: int,
    waste_type: str,
    weight: float,
    points: int,
    timestamp: Optional[datetime] = None
):
    log = models.WasteLog(
        user_id=user_id,
        waste_type=waste_type,
        weight=weight,
        points=points,
        timestamp=timestamp,  # if None, model default applies
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log

async def update_or_create_reward(
    db: AsyncSession,
    *,
    user_id: int,
    points_to_add: int
):
    result = await db.execute(select(models.Reward).filter(models.Reward.user_id == user_id))
    reward = result.scalars().first()
    if reward:
        reward.points = (reward.points or 0) + points_to_add
    else:
        reward = models.Reward(user_id=user_id, points=points_to_add, redeemed=False)
        db.add(reward)
    await db.commit()
    await db.refresh(reward)
    return reward

async def create_pickup(
    db: AsyncSession,
    *,
    household_id: int,
    worker_id: int
):
    pickup = models.Pickup(
        household_id=household_id,
        worker_id=worker_id,
        status=models.PickupStatus.pending,
    )
    db.add(pickup)
    await db.commit()
    await db.refresh(pickup)
    return pickup

async def update_pickup_status(
    db: AsyncSession,
    *,
    pickup_id: int,
    new_status: models.PickupStatus
):
    pickup = await get_pickup_by_id(db, pickup_id)
    if not pickup:
        return None
    pickup.status = new_status
    await db.commit()
    await db.refresh(pickup)
    return pickup