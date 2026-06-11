from fastapi import FastAPI
from app.core.database import Base, engine
from app.api.routes.habits import router as habits_router
from app.api.routes.stats import router as stats_router
from app.api.routes.auth import router as auth_router

def create_app() -> FastAPI:
    app = FastAPI(title="Habit Tracker API")

    # создаём таблицы (для MVP без alembic)
    Base.metadata.create_all(bind=engine)

    app.include_router(habits_router)
    app.include_router(stats_router)
    app.include_router(auth_router)
    
    return app

app = create_app()