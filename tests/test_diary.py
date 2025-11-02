import pytest
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

from app.main import app


@pytest.fixture(scope="module", autouse=True)
def initialize_tests():
    # 🧩 테스트용 임시 DB 세팅 (메모리 DB)
    initializer(["app.models.diary"], db_url="sqlite://:memory:", app_label="models")
    yield
    finalizer()


@pytest.mark.asyncio
async def test_create_diary():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"title": "테스트 제목", "content": "테스트 내용"}
        response = await ac.post("/diaries/", json=data)
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "테스트 제목"


@pytest.mark.asyncio
async def test_get_all_diaries():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/diaries/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
