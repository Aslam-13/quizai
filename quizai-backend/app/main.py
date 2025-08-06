# app/main.py

from fastapi import FastAPI
from app.api.v1 import quiz
from app.db.session import test_db_connection
from app.db.session import get_db
from app.db.sample_data import insert_sample_data
app = FastAPI()

# Health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Server running"}

# DB test
@app.get("/db-test")
async def db_test():
    result = await test_db_connection()
    return result

@app.on_event("startup")
async def startup_event():
    async for db in get_db():
        await insert_sample_data(db)
        break  

# API routers
app.include_router(quiz.router, prefix="/v1", tags=["Quiz"])