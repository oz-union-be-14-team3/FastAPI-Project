from pydantic import BaseModel
from datetime import datetime


class QuestionBase(BaseModel):
    question_text: str


class QuestionCreate(QuestionBase):
    """크롤링에 사용 예쩡"""
    pass


class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class UserQuestionBase(BaseModel):
    pass 


class UserQuestionCreate(UserQuestionBase):
    user_id: int
    question_id: int


class UserQuestionResponse(UserQuestionBase):
    id: int
    user_id: int
    question_id: int
    created_at: datetime
    question: QuestionResponse | None = None 

    class Config:
        from_attributes = True