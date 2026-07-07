from fastapi import FastAPI
import app
from app.core.database import Base, engine
from app.api.routes.habits import router as habits_router
from app.api.routes.stats import router as stats_router
from app.api.routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(title="Habit Tracker API")

    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    # создаём таблицы (для MVP без alembic)
    Base.metadata.create_all(bind=engine)

    app.include_router(habits_router)
    app.include_router(stats_router)
    app.include_router(auth_router)
    
    return app

    app = create_app()