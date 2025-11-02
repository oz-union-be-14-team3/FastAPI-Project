from pydantic import BaseModel
from datetime import datetime


class DiaryCreate(BaseModel):
    title: str
    content: str


class DiaryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class DiaryOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
