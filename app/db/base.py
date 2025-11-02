from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings


def db_connection(app):
    register_tortoise(
        app,
        db_url=settings.DB_URL,
        modules={"models": ["app.models"]},
        generate_schemas=False,
        add_exception_handlers=True
    )
