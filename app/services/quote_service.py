# import httpx
from bs4 import BeautifulSoup
from app.repositories.quote_repo import QuoteRepository
from app.core.config import settings
from app.models.quote import Quote
from typing import Optional, List, Dict
from playwright.async_api import async_playwright

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
        html_content = await self._fetch_html(self.scrape_url)
        if not html_content:
            return 0

        # 2. 파싱 실행 (Parser 호출)
        parsed_data: List[Dict[str, str]] = self._parse_quotes_from_html(html_content)

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

    async def _fetch_html(self, url: str) -> Optional[str]:
        """
        주어진 URL에서 HTML 내용을 Playwright를 사용하여 JavaScript가 로드된 후의 HTML 내용을 가져옵니다.
        추후 주석의 코드로 대체될 가능성이 높습니다. (임시)
        """
        async with async_playwright() as p:
            # Chromium 브라우저를 헤드리스 모드로 시작
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                print(f"Playwright: URL {url} 로딩 시작...")
                await page.goto(url)

                # 명언 태그가 로딩될 때까지 기다림
                # HTML 이미지에서 확인한 명언 태그인 'div.quote'가 최소 하나 나올 때까지 기다립니다.
                await page.wait_for_selector('div.quote')

                # 로딩이 완료된 후, 페이지의 최종 HTML을 가져옵니다.
                html_content = await page.content()
                print("Playwright: HTML 로딩 및 동적 콘텐츠 로드 완료.")
                return html_content

            except Exception as e:
                print(f"Playwright 오류 발생: {e}")
                return None

            finally:
                await browser.close()
        ''' 기존코드
        async with httpx.AsyncClient() as client:
            try:
                # 기본 설정 (타임아웃 포함)
                response = await client.get(url, timeout=10)
                response.raise_for_status()

                return response.text

            except httpx.HTTPStatusError as e:
                print(f"Fetcher HTTP Error: {e.response.status_code} on {url}")
                return None
            except Exception as e:
                print(f"Fetcher Network Error: {e}")
                return None
        '''

    def _parse_quotes_from_html(self, html_content: str) -> List[Dict[str, str]]:
        """
        HTML 문자열을 받아 명언과 작성자를 파싱하여 리스트로 반환.
        """
        if not html_content:
            return []

        quotes_data: List[Dict[str, str]] = []

        # 파싱 시작
        soup = BeautifulSoup(html_content, 'lxml')

        # 사이트의 원하는 셀렉터를 알아와 고쳐야합니다. (임시)
        for element in soup.find_all('div', class_='quote'):  # 임시. quote-card로 변경
            try:
                quote_text = element.find('p', class_='message').get_text(strip=True) # 임시. quote_message로 변경
                author_name = element.find('p', class_='author').get_text(strip=True) # 임시. author_name로 변경

                quotes_data.append({
                    "content": quote_text,
                    "author": author_name
                })
            except AttributeError:
                # 파싱 실패시 건너뜁니다.
                continue

        return quotes_data