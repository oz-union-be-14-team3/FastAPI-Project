from fastapi import APIRouter, Depends, HTTPException, status
from app.services.question_service import QuestionService, UserQuestionService
from app.repositories.question_repo import QuestionRepository, UserQuestionRepository
from app.schemas.question import QuestionResponse, UserQuestionResponse
from app.core.dependencies import get_current_user
from app.models.user import User
from tortoise.exceptions import DoesNotExist
from typing import List

router = APIRouter(prefix="/questions", tags=["Question"])

# 의존성 주입
def get_question_service() -> QuestionService:
    repo = QuestionRepository()
    return QuestionService(repository=repo)

def get_user_question_service() -> UserQuestionService:
    repo = UserQuestionRepository()
    return UserQuestionService(repository=repo)



# API 엔드포인트

@router.get("/list", response_model=List[QuestionResponse], summary="모든 질문 조회")
async def get_all_questions(service: QuestionService = Depends(get_question_service)):
    """
    DB에 저장된 모든 질문을 반환합니다.
    """
    questions = await service.get_all_questions()
    return questions


@router.get("/random", response_model=QuestionResponse, summary="랜덤 질문 하나 조회")
async def get_random_question(service: QuestionService = Depends(get_question_service)):
    """
    DB에 저장된 질문 중 하나를 랜덤으로 반환합니다.
    """
    question = await service.get_random_question()
    if not question:
        raise HTTPException(status_code=404, detail="No questions found in database")
    return question


@router.post("/scrape", summary="질문을 스크래핑하고 DB에 저장")
async def trigger_scraping(service: QuestionService = Depends(get_question_service)):
    """
    외부 사이트에서 질문을 스크래핑하고, 중복 없이 DB에 저장합니다.
    """
    saved_count = await service.save_scraping()
    return {"message": "스크래핑 및 저장 완료", "saved_count": saved_count}


@router.post("/assign", response_model=UserQuestionResponse, summary="유저에게 랜덤 질문 배정")
async def assign_question_to_user(
    q_service: QuestionService = Depends(get_question_service),
    uq_service: UserQuestionService = Depends(get_user_question_service),
    current_user: User = Depends(get_current_user),
):
    """
    로그인된 유저에게 랜덤 질문을 배정하고 DB에 기록합니다.
    """
    question = await q_service.get_random_question()
    if not question:
        raise HTTPException(status_code=404, detail="질문이 데이터베이스에 없습니다.")

    user_question, _ = await uq_service.assign_question_to_user(current_user, question)
    return user_question


@router.get("/me", response_model=List[UserQuestionResponse], summary="내가 받은 모든 질문 조회")
async def get_my_questions(
    service: UserQuestionService = Depends(get_user_question_service),
    current_user: User = Depends(get_current_user),
):
    """
    현재 로그인한 유저가 받은 모든 질문을 반환합니다.
    """
    return await service.get_user_questions(current_user)


@router.get("/me/latest", response_model=UserQuestionResponse, summary="가장 최근 질문 조회")
async def get_my_latest_question(
    service: UserQuestionService = Depends(get_user_question_service),
    current_user: User = Depends(get_current_user),
):
    """
    유저가 마지막으로 받은 질문을 반환합니다.
    """
    latest = await service.get_latest_user_question(current_user)
    if not latest:
        raise HTTPException(status_code=404, detail="최근 받은 질문이 없습니다.")
    return latest