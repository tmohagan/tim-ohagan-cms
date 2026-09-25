from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.pydantic_schemas import ProfileCreate, ProfileResponse
from app.models.sql_models import Profile
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    profile_data = profile.model_dump()
    if profile_data.get("github_url"):
        profile_data["github_url"] = str(profile_data["github_url"])
        
    db_profile = Profile(**profile_data)
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.id == profile_id))
    profile = result.scalars().first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
