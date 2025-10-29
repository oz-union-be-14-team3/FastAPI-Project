from pydantic import BaseModel


class Test(BaseModel):
    id : int
    question_text: str