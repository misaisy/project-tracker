from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from ..db.models import Project
from ..schemas.project import ProjectUpdate


async def create_project(db: AsyncSession, project_data: dict, owner_id: int) -> Project:
    db_project = Project(**project_data, owner_id=owner_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    return db_project


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    result = await db.execute(select(Project).filter(Project.id == project_id))
    return result.scalars().first()


async def get_user_projects(db: AsyncSession, user_id: int) -> list[Project]:
    result = await db.execute(select(Project).filter(Project.owner_id == user_id))
    return result.scalars().all()


async def update_project(db: AsyncSession, project: Project, update_data: ProjectUpdate) -> Project:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int) -> None:
    await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()