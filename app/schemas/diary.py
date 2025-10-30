from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DiaryCreate(BaseModel):
    title: Optional[str] = None
    content: str

class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class DiaryResponse(BaseModel):
    id: int
    title: Optional[str]
    content: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
