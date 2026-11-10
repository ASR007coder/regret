
# backend/app/run.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# routers

from backend.app.routers.health import router as health_router
from backend.app.routers.auth import router as auth_router
from backend.app.routers.feed import router as feed_router
from backend.app.routers.createQuestion import router as question_router
from backend.app.routers.createAnswer import router as answer_router
from backend.app.routers.me import router as me_router


# database

from backend.database.connection import engine
from backend.database.model import Base
from backend.database import model  # Register all models




app = FastAPI(
    title="Regret App",
    description="Anonymous regret sharing platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# creating table

Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {
        "message": "Welcome to REGRET API",
        "status": "running"
    }

# all routers

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(feed_router)
app.include_router(question_router)
app.include_router(answer_router)
app.include_router(me_router)


if __name__ == "__main__":

    uvicorn.run(
        "backend.app.run:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
