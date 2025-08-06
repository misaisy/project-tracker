from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..db.session import get_db
from ..crud.user import get_users, get_user, delete_user
from ..schemas.user import UserOut
from ..utils.dependencies import get_current_user, get_current_admin
from ..db.models import User

router = APIRouter()

@router.get("/me", response_model=UserOut, summary="Get current user info")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Получение информации о текущем аутентифицированном пользователе"""
    return UserOut.model_validate(current_user)

@router.get("/", response_model=list[UserOut], summary="Get all users (admin only)")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Получение списка всех пользователей (только для администратора)"""
    users = await get_users(db)
    return [UserOut.model_validate(user) for user in users]

@router.get("/{user_id}", response_model=UserOut, summary="Get user by ID (admin only)")
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Получение информации о пользователе по ID (только для администратора)"""
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserOut.model_validate(user)

@router.delete("/{user_id}", response_model=dict, summary="Delete user (admin only)")
async def delete_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Удаление пользователя по ID (только для администратора)"""
    deleted_user = await delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}