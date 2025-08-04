from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..crud.project import create_project as crud_create_project, get_user_projects, get_project
from ..schemas.project import ProjectCreate, ProjectOut
from ..utils.dependencies import get_current_user, get_current_project_owner
from ..schemas.user import UserOut

router = APIRouter()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создание нового проекта для текущего пользователя.
    """
    return await crud_create_project(db, project_data.model_dump(), current_user.id)

@router.get("/", response_model=list[ProjectOut])
async def get_projects(
    current_user: UserOut = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение списка всех проектов, принадлежащих текущему пользователю.
    """
    return await get_user_projects(db, current_user.id)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_detail(
    project: ProjectOut = Depends(get_current_project_owner)
):
    """
    Получение одного проекта по ID.
    """
    return project