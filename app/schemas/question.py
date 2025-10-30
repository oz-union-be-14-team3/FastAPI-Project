from pydantic import BaseModel
from datetime import datetime

class QuestionBase(BaseModel):
    question_text: str

class QuestionResponse(QuestionBase):
    id: int

    class Config:
        # Pydantic이 ORM 객체(Tortoise Model)에서 데이터를 읽을 수 있게 합니다.
        from_attributes = True

class UserQuestionBase(BaseModel):
    pass # 추가 필드 없음

class UserQuestionResponse(UserQuestionBase):
    id: int
    user_id: int
    quote_id: int
    created_at: datetime

    class Config:
        # Tortoise ORM 객체와 Pydantic 호환을 위한 설정
        from_attributes = True