from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..crud.user import get_user_by_email, create_user, update_user
from ..schemas.user import UserCreate, UserLogin, Token, UserOut, LogoutResponse, TokenRefresh, PasswordUpdate
from ..core.security import verify_password, create_access_token, get_password_hash, revoke_refresh_token, decode_token, \
    verify_refresh_token
from ..utils.dependencies import get_current_user


router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]

    return await create_user(db, user_dict)


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация пользователя и выдача JWT.
    """
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout", response_model=LogoutResponse)
async def logout(
        current_user: UserOut = Depends(get_current_user)
):
    """
    Выход из системы: отзывает refresh токен
    """
    revoke_refresh_token(current_user.id)
    return {"message": "Successfully logged out"}


@router.post("/refresh_token", response_model=Token)
async def refresh_token(
        token_data: TokenRefresh,
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление токена доступа с помощью refresh токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token_data.refresh_token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(db, email)
    if user is None or not verify_refresh_token(user.id, token_data.refresh_token):
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/update_password", response_model=LogoutResponse)
async def update_password(
        password_data: PasswordUpdate,
        current_user: UserOut = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление пароля пользователя
    """
    user = await get_user_by_email(db, current_user.email)
    if not verify_password(password_data.current_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    new_hashed_password = get_password_hash(password_data.new_password)

    await update_user(db, user, {"hashed_password": new_hashed_password})

    revoke_refresh_token(user.id)

    return {"message": "Password updated successfully"}