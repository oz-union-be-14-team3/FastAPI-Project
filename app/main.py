from fastapi import FastAPI
from app.db.base import db_connection
import uvicorn

app = FastAPI()

db_connection(app)

@app.get("/")
async def root():
    return {"ok": True}

if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
