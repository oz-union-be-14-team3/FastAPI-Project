from typing import Dict, List, Optional, Tuple

from tortoise.transactions import in_transaction

from app.models.bookmark import Bookmark
from app.models.quote import Quote
from app.models.user import User


# 데이터베이스 CRUD 쿼리를 직접 실행하고 파이썬 객체를 반환.
class QuoteRepository:
    """
        Quote 모델에 대한 데이터 접근 로직 관리
    """

    @staticmethod
    async def get_or_create_quote(data: Dict[str, str]) -> Tuple[Quote, bool]:
        """
        명언 내용(content)을 기준으로 존재하면 가져오고, 없다면 만듭니다.
        데이터를 파싱해와서 검색내용 없으면 그대로 저장시킵니다.
        """
        quote_obj, created = await Quote.get_or_create(
            content=data['content'],
            defaults={"author": data.get('author', '익명')}
        )
        return quote_obj, created

    @staticmethod
    async def delete_all_quotes() -> int:
        """
        명언 테이블의 모든 데이터를 삭제합니다.
        :return: int 삭제된 명언의 수
        """
        return await Quote.all().delete()

    @staticmethod
    async def get_all_quotes() -> List[Quote]:
        """
        명언테이블의 모든 명언을 조회합니다.
        """
        return await Quote.all()

    @staticmethod
    async def get_random_quote() -> Optional[Quote]:
        """
        데이터베이스에서 명언 하나를 랜덤으로 가져옵니다.
        (PostgreSQL용 Raw SQL 사용)
        """
        # ⭐️ Raw SQL을 실행하여 랜덤 ID를 가진 명언 하나를 조회합니다.
        async with in_transaction() as connection:
            # 랜덤 정렬 후 LIMIT 1 만 가져옴. (id, content, author)
            result = await connection.execute_query(
                "SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1"
            )

            # Quote 객체로 변환.
            if result and result[1]:
                # 결과 행을 딕셔너리로 변환 >  Quote 모델에 로드
                row = result[1][0]
                return Quote(id=row[0], content=row[1], author=row[2])

        return None


class BookmarkRepository:
    """
    북마크 모델에 대한 데이터 접근 로직 관리
    """

    @staticmethod
    async def get_or_create_bookmark(user: User, quote_obj: Quote) -> Tuple[Bookmark, bool]:
        """
        주어진 User 객체와 Quote 객체로 북마크를 찾거나 새로 생성합니다.

        :param user: 현재 로그인된 User 객체
        :param quote_obj: 북마크할 Quote 객체
        :return: 생성되거나 찾아진 Bookmark 객체와 생성 여부(True/False)
        """
        # 중복 북마크를 방지 및 생성/조회 처리.
        bookmark_obj, created = await Bookmark.get_or_create(
            user=user,
            quote=quote_obj,
            defaults={}  # 추가로 업데이트할 필드가 없으므로 빈 dict
        )

        return bookmark_obj, created
