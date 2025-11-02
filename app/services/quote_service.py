from app.repositories.quote_repo import QuoteRepository, BookmarkRepository
from app.core.config import settings
from app.models.quote import Quote
from app.models.bookmark import Bookmark
from app.scraping.quote_scraper import fetch_html, parse_quotes_from_html
from typing import Optional, List, Dict, Tuple
from tortoise.exceptions import DoesNotExist
from app.models.user import User


class QuoteService:
    def __init__(self, repository: QuoteRepository):
        self.repository = repository
        self.scrape_url = settings.QUOTES_SCRAPE_TARGET_URL # config에서 URL 가져오기

    async def get_all_quotes(self) -> List[Quote]:
        return await self.repository.get_all_quotes()

    async def get_random_quote(self) -> Optional[Quote]:
        return await self.repository.get_random_quote()

    async def save_scraping(self)  -> int:
        """
        스크래핑을 실행하고 파싱된 데이터를 DB에 저장하는 서비스입니다.
        저장된 명언의 개수를 반환합니다.
        """
        # 1. Fetcher 호출
        html_content = await fetch_html(self.scrape_url)
        if not html_content:
            return 0

        # 2. 파싱 실행 (Parser 호출)
        parsed_data: List[Dict[str, str]] = parse_quotes_from_html(html_content)

        # 3. Repository 호출 > DB 저장
        saved_count = 0
        for data in parsed_data:
            try:
                # 레포지토리에 저장 요청
                quote_obj, created = await self.repository.get_or_create_quote(data)

                # 저장 성공시 카운트 증가
                if created:
                    saved_count += 1

            except Exception as e:
                # DB 저장 중 오류가 발생하면 (예: 데이터 타입 불일치 등) 로깅하고 건너뜁니다.
                print(f"DB 저장 중 오류 발생: {data['content']} - {e}")
                continue
        return saved_count

    async def delete_all_quotes(self) -> int:
        """
        명언 테이블의 모든 데이터를 지웁니다
        :return: int 삭제된 명언의 수
        """
        return self.repository.delete_all_quotes()

class BookmarkService:
    def __init__(self, repository: BookmarkRepository):
        self.repository = repository

    async def add_or_get_bookmark(self, user: User, quote_id: int) -> Tuple[Bookmark, bool]:
        """
        명언 ID를 사용해 명언을 찾고, 북마크를 생성하거나 기존 것을 반환합니다.
        """

        # 명언 존재 여부 확인 가져오거나 none이거나
        quote_obj = await Quote.get_or_none(id=quote_id)

        if not quote_obj:
            # 명언이 존재하지 않으면 예외 발생
            raise DoesNotExist(f"ID {quote_id}를 가진 명언을 찾을 수 없습니다.")

        # 유효한 명언 객체를 Repository(북마크)에 전달하여 북마크 처리
        bookmark_obj, created = await self.repository.get_or_create_bookmark(
            user=user,
            quote_obj=quote_obj
        )

        return bookmark_obj, created