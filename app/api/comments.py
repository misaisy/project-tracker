from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..crud.comment import create_comment, get_task_comments
from ..crud.task import get_task as get_task_crud
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

    return await create_comment(db, comment_data.model_dump(), task_id, current_user.id)


@router.get("/{task_id}/comments", response_model=list[CommentOut])
async def get_comments(
        task_id: int = Path(..., title="ID задачи"),
        db: AsyncSession = Depends(get_db)
):
    """
    Получение списка всех комментариев к задаче.
    """
    return await get_task_comments(db, task_id)