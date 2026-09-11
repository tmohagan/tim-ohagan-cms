from fastapi import APIRouter, HTTPException
from app.schemas.pydantic_schemas import ProfileCreate, ProfileResponse

router = APIRouter()

# Ephemeral in-memory allocation until PostgreSQL integration
_mock_db = {}

@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(profile: ProfileCreate):
    new_id = len(_mock_db) + 1
    profile_data = profile.model_dump()
    profile_data["id"] = new_id
    _mock_db[new_id] = profile_data
    return profile_data

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: int):
    if profile_id not in _mock_db:
        raise HTTPException(status_code=404, detail="Profile not found in memory")
    return _mock_db[profile_id]
