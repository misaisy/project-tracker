from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.session import init_db

from .api.auth import router as auth_router
from .api.projects import router as projects_router
from .api.tasks import router as tasks_router
from .api.comments import router as comments_router

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