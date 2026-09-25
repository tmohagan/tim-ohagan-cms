from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.schemas.pydantic_schemas import CommentCreate, CommentResponse
from app.models.sql_models import Comment, Post
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    # Verify post exists
    result = await db.execute(select(Post).where(Post.id == comment.post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    # Verify parent comment exists if provided
    if comment.parent_id is not None:
        parent_result = await db.execute(select(Comment).where(Comment.id == comment.parent_id))
        parent = parent_result.scalars().first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")

    db_comment = Comment(**comment.model_dump())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

@router.get("/post/{post_id}", response_model=List[CommentResponse])
async def list_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc()))
    comments = result.scalars().all()
    return comments
