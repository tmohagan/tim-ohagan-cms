from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

class ProfileBase(BaseModel):
    name: str = Field(..., max_length=100, description="The display name of the profile owner.")
    bio: str = Field(..., description="A short markdown-enabled biography.")
    github_url: Optional[HttpUrl] = Field(None, description="Valid URL pointing to a GitHub profile.")

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int

    class Config:
        from_attributes = True
