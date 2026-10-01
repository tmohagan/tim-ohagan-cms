from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional
from app.schemas.pydantic_schemas import PostCreate, PostResponse
from app.models.sql_models import Post, Profile
from app.core.database import get_db

router = APIRouter()

CATEGORY_METADATA = {
    "Autonomous SRE": {
        "slug": "autonomous-sre",
        "icon": "⚡",
        "description": "Self-healing architectures, automated MTTR reduction, and production agent mechanics."
    },
    "Chaos Engineering": {
        "slug": "chaos-engineering",
        "icon": "💥",
        "description": "Fault injection, synthetic reproduction sandboxes, and automated regression verification."
    },
    "Agentic Architecture": {
        "slug": "agentic-architecture",
        "icon": "🧠",
        "description": "Stateful orchestration, cyclic graphs with LangGraph, and deterministic state reducers."
    },
    "AI Security & Guardrails": {
        "slug": "ai-security",
        "icon": "🛡️",
        "description": "Compiler-level AST validation, bare except elimination, and zero-trust LLM patch synthesis."
    }
}

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

@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post.category, func.count(Post.id)).group_by(Post.category)
    )
    db_counts = {row[0]: row[1] for row in result.all() if row[0]}
    
    categories = []
    seen = set()
    for name, meta in CATEGORY_METADATA.items():
        categories.append({
            "name": name,
            "slug": meta["slug"],
            "icon": meta["icon"],
            "description": meta["description"],
            "count": db_counts.get(name, 0)
        })
        seen.add(name)
        
    for cat_name, count in db_counts.items():
        if cat_name not in seen:
            slug = cat_name.lower().replace(" ", "-")
            categories.append({
                "name": cat_name,
                "slug": slug,
                "icon": "📁",
                "description": f"Transmissions and insights on {cat_name}.",
                "count": count
            })
            
    return categories

@router.get("/", response_model=List[PostResponse])
async def list_posts(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Post).order_by(Post.created_at.desc())
    if category and category.lower() not in ("all", ""):
        matching_cat = None
        for name, meta in CATEGORY_METADATA.items():
            if meta["slug"] == category.lower() or name.lower() == category.lower():
                matching_cat = name
                break
        if matching_cat:
            query = query.where(Post.category == matching_cat)
        else:
            query = query.where(func.lower(Post.category) == category.lower())

    result = await db.execute(query.offset(skip).limit(limit))
    posts = result.scalars().all()
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
