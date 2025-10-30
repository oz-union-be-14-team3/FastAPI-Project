from pydantic import BaseModel


class QuestionResponse(BaseModel):
    question_text: str