# routers/albums.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)

@router.post("/", response_model=schemas.Album)
async def create_new_album(
    album: schemas.AlbumCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Creates a new album.
    - Requires authentication.
    - User must have the 'admin' or 'editor' role.
    """
    # --- ADDED: Role-based permission check ---
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create an album."
        )

    # Check if an album with this name already exists
    db_album = await crud.get_album_by_name(db, name=album.name)
    if db_album:
        raise HTTPException(status_code=400, detail="Album with this name already exists.")
    
    return await crud.create_album(db=db, album=album)

@router.get("/", response_model=List[schemas.Album])
async def read_all_albums(db: AsyncSession = Depends(get_db)):
    """
    Retrieves a list of all albums.
    - No authentication required.
    """
    albums = await crud.get_albums(db)
    return albums