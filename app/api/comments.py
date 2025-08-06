from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..crud.comment import create_comment, get_task_comments
from ..crud.task import get_task as get_task_crud
from ..crud.project import get_project as get_project_crud, get_project
from ..schemas.comment import CommentCreate, CommentOut
from ..utils.dependencies import get_current_user
from ..schemas.user import UserOut

router = APIRouter()


@router.post("/{task_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(
        comment_data: CommentCreate,
        task_id: int = Path(..., title="ID задачи"),
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Добавление комментария к задаче.
    """
    task = await get_task_crud(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    project = await get_project_crud(db, task.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to comment on this task"
        )

    return await create_comment(db, comment_data.model_dump(), task_id)

@router.get("/{task_id}/comments", response_model=list[CommentOut])
async def get_comments(
        task_id: int = Path(..., title="ID задачи"),
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение списка всех комментариев к задаче.
    """
    task = await get_task_crud(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    project = await get_project(db, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view comments for this task"
        )

    return await get_task_comments(db, task_id)