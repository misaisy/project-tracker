from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.models import User
from ..core.security import decode_token
from ..crud.project import get_project
from ..crud.user import get_user_by_email
from ..db.session import async_session
from ..schemas.user import UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_db() -> AsyncSession:
    """Генератор асинхронных сессий БД."""
    async with async_session() as session:
        yield session


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    """Получает текущего аутентифицированного пользователя из JWT токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if not payload:
        raise credentials_exception

    try:
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception

    if email is None:
        raise credentials_exception

    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_project_owner(
        project_id: int = Path(...),
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Проверяет, что текущий пользователь владеет проектом."""
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this project"
        )
    return project

async def get_current_admin(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Проверяет, является ли пользователь администратором
    """
    if current_user.email != "admin@example.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user