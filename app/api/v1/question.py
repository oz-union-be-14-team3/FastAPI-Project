from fastapi import APIRouter
from app.models.question import Question
from app.schemas.question import QuestionResponse
from app.repositories.question_repo import QuestionRepository
from random import choice

router = APIRouter(prefix="/question", tags=["Question CRUD"])

@router.get("/", response_model=QuestionResponse)
async def all():
    questions = await QuestionRepository.read_one_question()
    random_question = choice(questions)
    return random_question