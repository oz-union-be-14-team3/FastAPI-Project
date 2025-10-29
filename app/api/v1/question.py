from fastapi import APIRouter
from app.models.question import Question
from app.schemas.question import Test

router = APIRouter(prefix="/question", tags=["질문"])

@router.get("/", response_model=list[Test])
async def all():
    result = await Question.all()
    return result