from typing import Any, Coroutine

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from ..db.models import User
from ..core.security import get_password_hash
from ..schemas.user import UserUpdate


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def get_users(db: AsyncSession) -> list[User]:
    """Получение списка всех пользователей"""
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: dict) -> User:
    if 'password' in user_data:
        user_data['hashed_password'] = get_password_hash(user_data.pop('password'))

    is_admin = user_data.pop('is_admin', False)

    db_user = User(**user_data, is_admin=is_admin)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: User, update_data: UserUpdate) -> User:
    if not isinstance(update_data, dict):
        update_dict = update_data.model_dump(exclude_unset=True)
    else:
        update_dict = update_data

    if 'password' in update_dict:
        update_dict['hashed_password'] = get_password_hash(update_dict.pop('password'))

    for key, value in update_dict.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User)
        .options(selectinload(User.projects))
        .filter(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return user