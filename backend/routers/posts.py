# routers/posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
async def get_all_posts(
    skip: int = 0, 
    limit: int = 10, 
    album: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieves a list of posts with optional filtering and pagination.
    - search: Searches title, caption, and alt_text.
    - album: Filters by album name.
    - tag: Filters by tag name.
    """
    return await crud.get_posts(db, skip=skip, limit=limit, album=album, tag=tag, search=search)

@router.get("/{post_id}", response_model=schemas.Post)
async def get_a_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a single post by its ID and increments its view count.
    """
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Increment view count
    db_post.views += 1
    await db.commit()
    await db.refresh(db_post)
    
    return db_post

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Creates a new post.
    - Requires authentication.
    - The image must be uploaded first via the /images/upload/ endpoint.
    - The image_url and image_public_id from that upload must be included.
    """
    return await crud.create_post(db=db, post=post, author_id=current_user.id)

@router.put("/{post_id}", response_model=schemas.Post)
async def update_a_post(
    post_id: int,
    post_data: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Updates a post.
    - Requires authentication.
    - User must be the author of the post or an admin.
    """
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await crud.update_post(db=db, post_id=post_id, post_data=post_data)

@router.delete("/{post_id}")
async def delete_a_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Deletes a post.
    - Requires authentication.
    - Deletes the image from Cloudinary and the record from the database.
    - User must be the author of the post or an admin.
    """
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    await crud.delete_post(db=db, post_id=post_id)
    return {"message": "Post deleted successfully"}

@router.post("/{post_id}/like")
async def like_a_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Likes a post.
    - Requires authentication.
    """
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = await crud.get_like(db, user_id=current_user.id, post_id=post_id)
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked")
    
    await crud.create_like(db=db, user_id=current_user.id, post_id=post_id)
    return {"message": "Post liked successfully"}

@router.delete("/{post_id}/like")
async def unlike_a_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Unlikes a post.
    - Requires authentication.
    """
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud.delete_like(db=db, user_id=current_user.id, post_id=post_id)
    return {"message": "Post unliked successfully"}