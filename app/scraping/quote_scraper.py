# import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from typing import Optional, List, Dict


async def fetch_html(url: str) -> Optional[str]:
    """
    주어진 URL에서 HTML 내용을 Playwright를 사용하여 JavaScript가 로드된 후의 HTML 내용을 가져옵니다.
    추후 주석의 코드로 대체될 가능성이 있습니다. (임시)
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


def parse_quotes_from_html(html_content: str) -> List[Dict[str, str]]:
    """
    HTML 문자열을 받아 명언과 작성자를 파싱하여 리스트로 반환.
    """
    if not html_content:
        return []

    quotes_data: List[Dict[str, str]] = []

    # 파싱 시작 (html.parser와 달리 별도설치 필요. 성능빠름.)
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