# backend/routers/device.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import schemas
from database import get_db

router = APIRouter()

@router.post("/upload")
async def upload_from_device(
    log: schemas.WasteLogCreate,
    db: AsyncSession = Depends(get_db)
):
    print(f"Received data from device {log.device_id}: {log.weight}kg of {log.waste_type}")
    return {"message": "Data received successfully (placeholder)"}