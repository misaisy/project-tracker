from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from .crud.user import get_user
from .db.session import init_db

from .api.auth import router as auth_router
from .api.users import router as users_router
from .api.projects import router as projects_router
from .api.tasks import router as tasks_router
from .api.comments import router as comments_router

from .db.models import User

app = FastAPI(
    title="Project Tracker API",
    description="REST API для управления проектами и задачами",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["Аутентификация"])
app.include_router(users_router, prefix="/api/users", tags=["Пользователи"])
app.include_router(projects_router, prefix="/api/projects", tags=["Проекты"])
app.include_router(tasks_router, prefix="/api", tags=["Задачи"])
app.include_router(comments_router, prefix="/api", tags=["Комментарии"])



@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/api/healthcheck", tags=["Система"])
async def healthcheck():
    """Проверка работоспособности сервиса"""
    return {"status": "ok", "message": "Service is running"}

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Project Tracker API - используйте /api/docs для документации"}

@app.get("/test")
async def test():
    return {"message": "Test endpoint works"}


async def get_users(db: AsyncSession) -> list[User]:
    """Получение списка всех пользователей"""
    result = await db.execute(select(User))
    return result.scalars().all()


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """Удаление пользователя по ID"""
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()