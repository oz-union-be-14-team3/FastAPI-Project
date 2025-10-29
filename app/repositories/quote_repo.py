from typing import List, Dict, Tuple, Optional
from app.models.quote import Quote
from tortoise.transactions import in_transaction

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

    # 모든 명언 조회 (임시 함수입니다. **변경이 필요하며** 추후 삭제 또는 이관을 검토합니다.)
    @staticmethod
    async def get_all_quotes() -> List[Quote]:
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
            result = await connection.execute_query("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")

            # Quote 객체로 변환.
            if result and result[1]:
                # 결과 행을 딕셔너리로 변환 >  Quote 모델에 로드
                row = result[1][0]
                return Quote(id=row[0], content=row[1], author=row[2])

        return None