from app.api.v1 import auth, diary, quote, question
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI
from app.db.base import db_connection
import uvicorn


app = FastAPI(title="Diary CRUD API")

db_connection(app)

app.include_router(auth.router)
app.include_router(diary.router)
app.include_router(question.router)
app.include_router(quote.router)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Hello, world!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
