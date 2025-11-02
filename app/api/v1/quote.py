from fastapi import APIRouter, Depends, HTTPException, status
from app.services.quote_service import QuoteService, BookmarkService
from app.repositories.quote_repo import QuoteRepository, BookmarkRepository
from app.schemas.quote import QuoteResponse, BookmarkResponse
from tortoise.exceptions import DoesNotExist
from app.core.dependencies import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/quotes", tags=["Quote"])

# 요청 시마다 Repository와 Service 인스턴스를 생성하여 주입합니다.
def get_quote_service() -> QuoteService:
    repo = QuoteRepository()
    return QuoteService(repository=repo)

def get_bookmark_service() -> BookmarkService:
    repo = BookmarkRepository()
    return BookmarkService(repository=repo)

@router.get("/list", response_model=List[QuoteResponse], summary="모든 명언 조회")
async def get_quotes(service: QuoteService = Depends(get_quote_service)):
    """
    데이터베이스에 저장된 모든 명언 목록을 반환합니다.
    """
    quotes = await service.get_all_quotes()
    return quotes

@router.get("/random", response_model=QuoteResponse, summary="랜덤 명언 하나 조회")
async def get_random_quote(service: QuoteService = Depends(get_quote_service)):
    """
        데이터베이스에 저장된 명언 중 하나를 랜덤으로 반환합니다.
        """
    quote = await service.get_random_quote()

    # 명언 안 가져오면 404 error
    if quote is None:
        raise HTTPException(status_code=404, detail="No quotes found in database")

    return quote

@router.post("/scrape", summary="명언을 스크래핑하고 DB에 저장합니다.")
async def trigger_scraping(service: QuoteService = Depends(get_quote_service)):
    """
    외부 URL에서 명언을 스크래핑하고, 중복을 확인하며 DB에 저장합니다.
    """
    saved_count = await service.save_scraping()

    return {"message": "스크래핑 및 저장 완료", "saved_count": saved_count}

@router.delete("/delete_all", summary="저장된 명언을 모두 삭제합니다.")
async def delete_all_quotes(service: QuoteService = Depends(get_quote_service)):
    """
    quotes table의 모든 데이터를 삭제합니다.
    """
    delete_count = await service.delete_all_quotes()

    return {"message": "quotes의 모든 데이터 삭제 완료", "delete_count": delete_count}


@router.post("/{quote_id}/bookmark",response_model=BookmarkResponse,status_code=status.HTTP_201_CREATED,summary="명언 북마크 추가")
async def create_bookmark(quote_id: int, service: BookmarkService = Depends(get_bookmark_service), current_user: User = Depends(get_current_user)):
    """
    주어진 명언 ID를 현재 로그인된 사용자의 북마크에 추가합니다.
    이미 존재하는 경우, 기존 북마크를 반환합니다.
    """
    try:
        bookmark, created = await service.add_or_get_bookmark(
            user=current_user,
            quote_id=quote_id
        )

        # 이미존재
        if not created:
            return bookmark # 200 OK 상태 코드 반환

        # 새로 생성 : 201 Created
        return bookmark

    except DoesNotExist as e:
        # 명언이 존재하지 않을 경우 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception:
        # 기타 서버 오류 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process bookmark request."
        )