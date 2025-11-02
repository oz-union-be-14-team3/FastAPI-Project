from app.repositories.question_repo import QuestionRepository, UserQuestionRepository
from app.scraping.question_scraper import fetch_html, parse_questions_from_html
from app.models.question import Question
from app.models.user import User
from app.models.user_question import UserQuestion
from app.core.config import settings
from typing import Optional, List, Dict, Tuple


class QuestionService:
    def __init__(self, repository: QuestionRepository):
        self.repository = repository
        self.scrape_url = settings.QUESTION_SCRAPE_TARGET_URL

    async def get_all_questions(self) -> List[Question]:
        """모든 질문 반환"""
        return await self.repository.get_all_questions()

    async def get_random_question(self) -> Optional[Question]:
        """랜덤 질문 1개 반환"""
        return await self.repository.get_random_question()

    async def delete_all_questions(self) -> int:
        """
        질문 테이블의 모든 데이터를 지웁니다.
        :return: int 삭제된 질문의 수
        """
        return await self.repository.delete_all_questions()

    async def save_scraping(self) -> int:
        """
        스크래핑을 실행하고 파싱된 데이터를 DB에 저장하는 서비스입니다.
        저장된 질문의 개수를 반환합니다.
        """
        html_content = await fetch_html(self.scrape_url)
        if not html_content:
            return 0

        parsed_data: List[Dict[str, str]] = parse_questions_from_html(html_content)

        saved_count = 0
        for data in parsed_data:
            try:
                question_obj, created = await self.repository.get_or_create_question(data)
                if created:
                    saved_count += 1
            except Exception as e:
                print(f"DB 저장 중 오류 발생: {data['question_text']} - {e}")
                continue

        return saved_count


class UserQuestionService:
    def __init__(self, repository: UserQuestionRepository):
        self.repository = repository

    async def assign_question_to_user(
        self, user: User, question: Question
    ) -> Tuple[UserQuestion, bool]:
        # 유저에게 질문을 배정하고 기록을 남김
        uq, created = await self.repository.create_user_question(user, question)
        return uq, created

    async def get_user_questions(self, user: User) -> List[UserQuestion]:
        # 유저가 지금까지 받은 모든 질문 조회
        return await self.repository.get_user_questions(user)

    async def get_latest_user_question(self, user: User) -> Optional[UserQuestion]:
        # 유저의 가장 최근 질문 조회
        return await self.repository.get_latest_user_question(user)
