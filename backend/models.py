# backend/models.py

from sqlalchemy import (Column, Integer, String, Boolean, DateTime,
                        ForeignKey, Enum, Float)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    household = "household"
    worker = "worker"
    admin = "admin"

class PickupStatus(str, enum.Enum):
    pending = "pending"
    collected = "collected"

class DeviceStatus(str, enum.Enum):
    online = "online"
    offline = "offline"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    role = Column(Enum(UserRole))
    password_hash = Column(String) # Renamed from hashed_password

    # Relationships
    devices = relationship("Device", back_populates="owner")
    waste_logs = relationship("WasteLog", back_populates="owner")
    rewards = relationship("Reward", back_populates="owner")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(DeviceStatus), default=DeviceStatus.offline)

    owner = relationship("User", back_populates="devices")

class WasteLog(Base):
    __tablename__ = "waste_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    waste_type = Column(String)
    weight = Column(Float)
    points = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="waste_logs")

class Pickup(Base):
    __tablename__ = "pickups"
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("users.id"))
    household_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(PickupStatus), default=PickupStatus.pending)
    date = Column(DateTime(timezone=True), server_default=func.now())

    worker = relationship("User", foreign_keys=[worker_id])
    household = relationship("User", foreign_keys=[household_id])

class Reward(Base):
    __tablename__ = "rewards"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer)
    redeemed = Column(Boolean, default=False)

    owner = relationship("User", back_populates="rewards")