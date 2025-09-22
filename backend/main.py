# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from database import engine, Base
from routers import auth, household, worker, admin, device

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application startup...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables verified/created.")
    yield
    logging.info("Application shutdown.")

app = FastAPI(
    lifespan=lifespan,
    title="Waste Management API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- This section fixes the documentation issue ---
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(household.router, prefix="/api/household", tags=["Household"])
app.include_router(worker.router, prefix="/api/worker", tags=["Worker"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(device.router, prefix="/api/device", tags=["IoT Device"])
# ---------------------------------------------------

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "API is healthy"}