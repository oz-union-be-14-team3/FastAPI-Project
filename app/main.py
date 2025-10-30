from app.api.v1 import auth, diary, question
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
from app.db.base import db_connection
from app.scraping.question_scraper import QustionsScraper
from app.models.question import Question
import re
import uvicorn

from app.db.base import db_connection  

app = FastAPI(title="Diary CRUD API")

db_connection(app)

app.include_router(question.router)
app.include_router(auth.router)
app.include_router(diary.router)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Hello, world!"

@app.on_event("startup")
async def init_questions():
    url = "https://ksmb.tistory.com/entry/%EC%98%A4%EB%8A%98-%EB%82%98%EC%97%90%EA%B2%8C-%ED%95%98%EB%8A%94-%EC%A7%88%EB%AC%B8-%EB%8C%80%EB%8B%B5?utm_source=chatgpt.com"
    scraper = QustionsScraper(url)

    questions = await scraper.fetch_questions()

    for q in questions:
        clean_text = re.sub(r"^\d+\.\s*", "", q).strip()
        exists = await Question.filter(question_text=clean_text).exists()
        if not exists:
            await Question.create(question_text=clean_text)




if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
