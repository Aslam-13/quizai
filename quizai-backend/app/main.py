# app/main.py

from fastapi import FastAPI
from app.api.v1.routes import quiz
from app.db.session import test_db_connection

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


# API routers
app.include_router(quiz.router, prefix="/v1", tags=["Quiz"])