# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

import models
from database import engine, Base
from routers import auth, posts, comments, images, albums

# --- Lifespan event for startup/shutdown ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")
    async with engine.begin() as conn:
        # This creates the tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")
    yield
    logger.info("Application shutdown...")

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    lifespan=lifespan,
    title="CloneFest 2025 - Image Gallery API",
    description="A modern, extensible media platform API.",
    version="1.0.0"
)

# --- CORRECTED CORS Configuration ---
# This is the critical part. We are explicitly allowing your frontend's domain.
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "https://clonefest.up.railway.app", # Your deployed frontend URL
    "*" # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CORRECTED Router Configuration ---
# All routers now have a consistent "/api" prefix.
logger.info("Registering routers...")
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(images.router, prefix="/api/images", tags=["Images"])
app.include_router(albums.router, prefix="/api/albums", tags=["Albums"])
logger.info("Routers registered successfully.")


# --- Health Check Endpoint ---
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "message": "Image Gallery API is running", 
        "status": "healthy",
        "docs_url": "/docs"
    }


