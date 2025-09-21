# models.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

# --- New Enum for Post Privacy ---
# Using an Enum makes the privacy settings robust and less error-prone.
class PostPrivacy(str, enum.Enum):
    public = "public"
    unlisted = "unlisted"
    private = "private"

# --- New Enum for User Roles ---
# This fulfills the requirement for Admin, Editor, and Visitor roles.
class UserRole(str, enum.Enum):
    admin = "admin"
    editor = "editor"
    visitor = "visitor"

# Association table for many-to-many relationship between posts and tags
post_tags = Table(
    'post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    # --- MODIFIED: Using the new UserRole Enum ---
    role = Column(Enum(UserRole), default=UserRole.visitor)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")

# --- RENAMED: from Blog to Post ---
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    # --- ADDED: Fields for image metadata ---
    caption = Column(Text, nullable=True)
    alt_text = Column(String(255), nullable=True)
    
    # --- ADDED: Fields for Cloudinary integration ---
    image_url = Column(String(500), nullable=False)
    image_public_id = Column(String(255), nullable=False)

    # --- ADDED: Fields for hackathon requirements ---
    license = Column(String(100), nullable=True)
    privacy = Column(Enum(PostPrivacy), default=PostPrivacy.public)
    
    # --- KEPT: These are still useful ---
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # --- REMOVED: Unnecessary fields ---
    # content, content_type, content_format, media_path, published
    # media_content, media_filename, media_type are all handled by Cloudinary now.

    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"))
    # --- RENAMED: from category_id to album_id ---
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    album = relationship("Album", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    likes = relationship("Like", back_populates="post")

# --- RENAMED: from Category to Album ---
class Album(Base):
    __tablename__ = "albums"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    posts = relationship("Post", back_populates="album")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=True)
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"))
    # --- RENAMED: from blog_id to post_id ---
    post_id = Column(Integer, ForeignKey("posts.id"))
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    # --- RENAMED: from blog_id to post_id ---
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    # Relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")