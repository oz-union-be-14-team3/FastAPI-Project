# 테이블정보 입력
from pydantic import BaseModel

class QuoteBase(BaseModel):
    content: str
    author: str

class QuoteResponse(QuoteBase):
    id: int

    class Config:
        # Pydantic이 ORM 객체(Tortoise Model)에서 데이터를 읽을 수 있게 합니다.
        from_attributes = True