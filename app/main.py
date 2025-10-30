from app.api.v1 import auth, diary

from fastapi import FastAPI
from app.db.base import db_connection
from app.api.v1.question import router
from app.scraping.question_scraper import QustionsScraper
from app.models.question import Question
import re
import uvicorn

from app.db.base import db_connection  

app = FastAPI(title="Diary CRUD API")

db_connection(app)

app.include_router(router)
app.include_router(auth.router)
app.include_router(diary.router)



@app.get("/")
async def root():
    return {"ok": True}



if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
