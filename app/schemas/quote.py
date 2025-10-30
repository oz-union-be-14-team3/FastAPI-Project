# 테이블정보 입력
from pydantic import BaseModel
from datetime import datetime

class QuoteBase(BaseModel):
    content: str
    author: str

class QuoteResponse(QuoteBase):
    id: int

    class Config:
        # Pydantic이 ORM 객체(Tortoise Model)에서 데이터를 읽을 수 있게 합니다.
        from_attributes = True

class BookmarkBase(BaseModel):
    pass # 추가 필드 없음

class BookmarkResponse(BookmarkBase):
    id: int
    user_id: int
    quote_id: int
    created_at: datetime

    class Config:
        # Tortoise ORM 객체와 Pydantic 호환을 위한 설정
        from_attributes = True