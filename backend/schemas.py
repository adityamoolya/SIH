# backend/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import UserRole, DeviceStatus, PickupStatus

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Device Schemas ---
class Device(BaseModel):
    id: int
    device_id: str
    user_id: int
    status: DeviceStatus
    class Config:
        from_attributes = True

# --- WasteLog Schemas ---
class WasteLogBase(BaseModel):
    waste_type: str
    weight: float

class WasteLogCreate(WasteLogBase):
    device_id: str
    timestamp: datetime

class WasteLog(WasteLogBase):
    id: int
    user_id: int
    points: int
    timestamp: datetime
    class Config:
        from_attributes = True

# --- Pickup Schemas ---
class Pickup(BaseModel):
    id: int
    worker_id: int
    household_id: int
    status: PickupStatus
    date: datetime
    class Config:
        from_attributes = True

# --- Reward Schemas ---
class Reward(BaseModel):
    id: int
    user_id: int
    points: int
    redeemed: bool
    class Config:
        from_attributes = True

# --- Analytics Schemas ---
class AdminAnalytics(BaseModel):
    total_waste_collected: float
    segregation_accuracy: float # As a percentage
    active_households: int