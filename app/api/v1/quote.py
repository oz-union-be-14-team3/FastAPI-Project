from fastapi import APIRouter, Depends, HTTPException
from app.services.quote_service import QuoteService
from app.repositories.quote_repo import QuoteRepository
from app.schemas.quote import QuoteResponse
from typing import List

router = APIRouter()

# 요청 시마다 Repository와 Service 인스턴스를 생성하여 주입합니다.
def get_quote_service() -> QuoteService:
    repo = QuoteRepository()
    return QuoteService(repository=repo)

@router.get("/quotes_list", response_model=List[QuoteResponse], summary="모든 명언 조회")
async def get_quotes(service: QuoteService = Depends(get_quote_service)):
    """
    데이터베이스에 저장된 모든 명언 목록을 반환합니다.
    """
    quotes = await service.get_all_quotes()
    return quotes

@router.get("/random_quote", response_model=QuoteResponse, summary="랜덤 명언 하나 조회")
async def get_random_quote_endpoint(service: QuoteService = Depends(get_quote_service)):
    """
        데이터베이스에 저장된 명언 중 하나를 랜덤으로 반환합니다.
        """
    quote = await service.get_random_quote()

    # 명언 안 가져오면 404 error
    if quote is None:
        raise HTTPException(status_code=404, detail="No quotes found in database")

    return quote

@router.post("/quotes_scrape", summary="명언을 스크래핑하고 DB에 저장합니다.")
async def trigger_scraping(
        service: QuoteService = Depends(get_quote_service)
):
    """
    외부 URL에서 명언을 스크래핑하고, 중복을 확인하며 DB에 저장합니다.
    """
    saved_count = await service.save_scraping()

    return {"message": "스크래핑 및 저장 완료", "saved_count": saved_count}