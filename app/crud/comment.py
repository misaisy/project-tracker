from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from ..db.models import Comment
from ..schemas.comment import CommentUpdate


async def create_comment(db: AsyncSession, comment_data: dict, task_id: int) -> Comment:
    db_comment = Comment(**comment_data, task_id=task_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comment(db: AsyncSession, comment_id: int) -> Comment | None:
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    return result.scalars().first()


async def get_task_comments(db: AsyncSession, task_id: int) -> list[Comment]:
    result = await db.execute(select(Comment).filter(Comment.task_id == task_id))
    return result.scalars().all()


async def update_comment(db: AsyncSession, comment: Comment, update_data: CommentUpdate) -> Comment:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(comment, key, value)

    await db.commit()
    await db.refresh(comment)
    return comment


async def delete_comment(db: AsyncSession, comment_id: int) -> None:
    await db.execute(delete(Comment).where(Comment.id == comment_id))
    await db.commit()