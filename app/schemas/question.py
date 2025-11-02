from datetime import datetime

from pydantic import BaseModel


class QuestionBase(BaseModel):
    question_text: str


class QuestionCreate(QuestionBase):
    """
    새로운 질문을 추가할 때 사용하는 모델 (크롤링 시에도 사용)
    """
    pass


class QuestionResponse(QuestionBase):
    """
    랜덤으로 선택된 질문을 유저에게 반환할 때 사용하는 응답 모델
    """
    id: int

    class Config:
        from_attributes = True


class UserQuestionBase(BaseModel):
    pass


class UserQuestionCreate(UserQuestionBase):
    """
    유저가 질문을 받았을 때, 해당 유저-질문 관계를 생성하는 요청 모델
    """
    user_id: int
    question_id: int


class UserQuestionResponse(UserQuestionBase):
    """
    유저가 받은 질문 정보를 반환할 때 사용하는 응답 모델
    """
    id: int
    user_id: int
    question_id: int
    created_at: datetime
    question: QuestionResponse | None = None 

    class Config:
        from_attributes = True
