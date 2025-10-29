from fastapi import FastAPI
import uvicorn

from app.api import diary_router
from app.db.session import db_connection  # ← DB 연결 함수가 있다면 유지
# from app.db.dependencies import get_db  ← 의존성 주입용 (필요시)

app = FastAPI(title="Diary CRUD API")

#  DB 연결 (있다면 이 부분 유지)
db_connection(app)

#  기본 라우트
@app.get("/")
async def root():
    return {"ok": True}

# 라우터 등록
app.include_router(diary_router.router)

#  메인 실행 부분 (맨 아래)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
