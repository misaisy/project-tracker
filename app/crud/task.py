from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from ..db.models import Task


async def create_task(db: AsyncSession, task_data: dict, project_id: int) -> Task:
    db_task = Task(**task_data, project_id=project_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()


async def get_project_tasks(db: AsyncSession, project_id: int) -> list[Task]:
    result = await db.execute(select(Task).filter(Task.project_id == project_id))
    return result.scalars().all()


async def update_task(db: AsyncSession, task: Task, update_data: dict) -> Task:
    for key, value in update_data.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int) -> None:
    await db.execute(delete(Task).where(Task.id == task_id))
    await db.commit()