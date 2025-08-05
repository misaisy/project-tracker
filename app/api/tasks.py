from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..crud.task import create_task, get_project_tasks, get_task, update_task, delete_task
from ..crud.project import get_project as get_project_crud
from ..schemas.task import TaskCreate, TaskOut, TaskUpdate
from ..utils.dependencies import get_current_user, get_current_project_owner
from ..schemas.project import ProjectOut
from ..schemas.user import UserOut

router = APIRouter()


@router.post("/{project_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
        task_data: TaskCreate,
        project: ProjectOut = Depends(get_current_project_owner),
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Создание новой задачи в указанном проекте.
    """
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this task"
        )
    return await create_task(db, task_data.model_dump(), project.id)


@router.get("/{project_id}/tasks", response_model=list[TaskOut])
async def get_tasks(
        project: ProjectOut = Depends(get_current_project_owner),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение списка всех задач в проекте.
    """
    return await get_project_tasks(db, project.id)


@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task_endpoint(
        update_data: TaskUpdate,
        task_id: int = Path(..., title="ID задачи"),
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление задачи (например, смена статуса).
    """
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    project = await get_project_crud(db, task.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this task"
        )

    return await update_task(db, task, update_data.model_dump())


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
        task_id: int = Path(..., title="ID задачи"),
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Удаление задачи.
    """
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    project = await get_project_crud(db, task.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this task"
        )

    await delete_task(db, task_id)
    return {}