import asyncio
import re
from bs4 import BeautifulSoup
import requests

class QustionsScraper:
    
    def __init__(self, url:str):
        self.url = url
    
    async def fetch_questions(self):
        loop=asyncio.get_event_loop()

        res = await loop.run_in_executor(None, requests.get, self.url)
        res.encoding = "utf-8"

        soup = BeautifulSoup(res.text, "html.parser")

        questions = []
        for p in soup.find_all("p", {"data-ke-size":"size16"}):
            text = p.get_text(strip=True)
            if re.match(r"^\d+\.", text):
                questions.append(text)

        return questions
    

async def test():
    A = QustionsScraper(url="https://ksmb.tistory.com/entry/%EC%98%A4%EB%8A%98-%EB%82%98%EC%97%90%EA%B2%8C-%ED%95%98%EB%8A%94-%EC%A7%88%EB%AC%B8-%EB%8C%80%EB%8B%B5?utm_source=chatgpt.com")
    result = await A.fetch_questions()
    for r in result:
        print(r)

if __name__=="__main__":
    asyncio.run(test())