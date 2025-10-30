import re
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def fetch_html(url: str) -> Optional[str]:
    """
    주어진 URL에서 JavaScript가 렌더링된 후의 HTML을 가져옵니다.
    (Playwright 비동기 방식 사용)
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print(f"Playwright: URL {url} 로딩 시작...")
            await page.goto(url, timeout=15000)

            # <p data-ke-size="size16"> 요소가 로딩될 때까지 대기
            await page.wait_for_selector('p[data-ke-size="size16"]', timeout=10000)

            html_content = await page.content()
            print("Playwright: HTML 로딩 완료.")
            return html_content

        except Exception as e:
            print(f"Playwright 오류 발생: {e}")
            return None
        finally:
            await browser.close()


def parse_questions_from_html(html_content: str) -> List[Dict[str, str]]:
    """
    HTML에서 '오늘 나에게 하는 질문' 형식의 질문 리스트를 파싱합니다.
    (예: 1. 오늘 하루 중 가장 기뻤던 순간은?)
    """
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, "lxml")
    questions: List[Dict[str, str]] = []

    for p in soup.find_all("p", {"data-ke-size": "size16"}):
        text = p.get_text(strip=True)

        # 번호로 시작하는 경우만 질문으로 인식
        if re.match(r"^\d+\.", text):
            # 번호는 제거
            text = re.sub(r"^\d+\.\s*", "", text)
            questions.append({"question_text": text})

    print(f"총 {len(questions)}개의 질문을 파싱함.")
    return questions


if __name__ == "__main__":
    import asyncio

    async def test():
        url = "https://ksmb.tistory.com/entry/%EC%98%A4%EB%8A%98-%EB%82%98%EC%97%90%EA%B2%8C-%ED%95%98%EB%8A%94-%EC%A7%88%EB%AC%B8-%EB%8C%80%EB%8B%B5?utm_source=chatgpt.com"
        html = await fetch_html(url)
        questions = parse_questions_from_html(html)
        for q in questions:
            print(q["question_text"])

    asyncio.run(test())