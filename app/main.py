from fastapi import FastAPI
from app.db.base import db_connection
import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.api.v1 import auth, diary
from app.core.config import settings

app = FastAPI(title="FastAPI Mini Project")
db_connection(app)

app.include_router(auth.router)
app.include_router(diary.router)

@app.get("/")
async def root():
    return {"ok": True}

if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)