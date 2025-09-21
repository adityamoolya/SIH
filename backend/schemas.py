# schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
# --- IMPORTED: The Enums from our new models file ---
from models import PostPrivacy, UserRole

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr
    # --- MODIFIED: Using the UserRole Enum for validation ---
    role: UserRole = UserRole.visitor

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Authentication Schemas (No change needed) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- RENAMED: from Category to Album Schemas ---
class AlbumBase(BaseModel):
    name: str
    description: Optional[str] = None

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Tag Schemas (No change needed) ---
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    author: User
    # --- RENAMED: from blog_id to post_id ---
    post_id: int
    created_at: datetime
    is_approved: bool

    class Config:
        from_attributes = True

# --- RENAMED: from Blog to Post Schemas ---
class PostBase(BaseModel):
    title: str
    # --- ADDED: New fields for the hackathon requirements ---
    caption: Optional[str] = None
    alt_text: Optional[str] = None
    license: Optional[str] = None
    privacy: PostPrivacy = PostPrivacy.public
    album_id: Optional[int] = None

class PostCreate(PostBase):
    # --- MODIFIED: The create schema now needs the Cloudinary info ---
    image_url: str
    image_public_id: str
    tags: List[str] = []

class Post(PostBase):
    id: int
    author: User
    # --- MODIFIED: Now includes the Cloudinary URL ---
    image_url: str
    # --- RENAMED & MODIFIED: from category to album ---
    album: Optional[Album] = None
    tags: List[Tag] = []
    comments: List[Comment] = []
    views: int
    likes_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Like Schema ---
class Like(BaseModel):
    id: int
    user: User
    # --- RENAMED: from blog_id to post_id ---
    post_id: int

    class Config:
        from_attributes = True