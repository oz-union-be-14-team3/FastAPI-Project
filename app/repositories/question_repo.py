from typing import List, Tuple, Optional, Dict
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import in_transaction
from app.models.question import Question
from app.models.user_question import UserQuestion
from app.models.user import User


class QuestionRepository:
    """
    Question 모델 (질문 데이터) 접근 로직 관리
    """

    @staticmethod
    async def get_or_create_question(data: Dict[str, str]) -> Tuple[Question, bool]:
        """
        질문 내용(question_text)을 기준으로 존재하면 가져오고, 없다면 새로 생성합니다.
        (크롤링된 질문 중복 방지를 위해 사용)
        """
        question_obj, created = await Question.get_or_create(
            question_text=data["question_text"].strip()
        )
        return question_obj, created


    @staticmethod
    async def get_all_questions() -> List[Question]:
        """
        모든 질문을 조회합니다.
        """
        return await Question.all().order_by("-id")

    @staticmethod
    async def get_question_by_id(question_id: int) -> Optional[Question]:
        """
        ID로 특정 질문 하나를 조회합니다.
        """
        try:
            return await Question.get(id=question_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_random_question() -> Optional[Question]:
        """
        데이터베이스에서 질문 하나를 랜덤으로 가져옵니다.
        (PostgreSQL의 RANDOM() 사용)
        """
        async with in_transaction() as connection:
            result = await connection.execute_query(
                "SELECT id FROM questions ORDER BY RANDOM() LIMIT 1"
            )
            if result and result[1]:
                question_id = result[1][0][0]
                return await Question.get(id=question_id)
        return None


class UserQuestionRepository:
    """
    유저에게 질문이 배정될 때 사용하는 저장소.
    """

    @staticmethod
    async def create_user_question(user: User, question: Question) -> Tuple[UserQuestion, bool]:
        """
        유저가 질문을 받을 때 DB에 기록을 저장합니다.
        같은 질문을 여러 번 받을 수 있으므로 단순 생성만 수행.
        """
        uq = await UserQuestion.create(user=user, question=question)
        return uq, True

    @staticmethod
    async def get_user_questions(user: User) -> List[UserQuestion]:
        """
        유저가 지금까지 받은 모든 질문을 조회합니다.
        """
        return (
            await UserQuestion.filter(user=user)
            .prefetch_related("question")
            .order_by("-created_at")
        )

    @staticmethod
    async def get_latest_user_question(user: User) -> Optional[UserQuestion]:
        """
        유저가 가장 최근에 받은 질문을 조회합니다.
        """
        return (
            await UserQuestion.filter(user=user)
            .prefetch_related("question")
            .order_by("-created_at")
            .first()
        )