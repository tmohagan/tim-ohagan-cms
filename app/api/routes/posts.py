from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.schemas.pydantic_schemas import PostCreate, PostResponse
from app.models.sql_models import Post, Profile
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    # Verify author exists if provided
    if post.author_id is not None:
        result = await db.execute(select(Profile).where(Profile.id == post.author_id))
        author = result.scalars().first()
        if not author:
            raise HTTPException(status_code=404, detail="Author profile not found")

    db_post = Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostResponse])
async def list_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit))
    posts = result.scalars().all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
