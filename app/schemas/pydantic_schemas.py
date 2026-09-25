from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

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

class PostBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field(..., description="Markdown content of the post.")
    author_id: Optional[int] = Field(None)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    post_id: int
    author_name: str = Field(..., max_length=100)
    content: str
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
