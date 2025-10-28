from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.api.v1 import auth, diary
from app.core.config import settings

app = FastAPI(title="FastAPI Mini Project")

app.include_router(auth.router)
app.include_router(diary.router)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": ["app.models.user", "app.models.diary"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
