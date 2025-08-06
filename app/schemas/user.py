from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr = Field(..., example="user@example.com", description="Email пользователя")


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str = Field(..., min_length=6, example="strongpassword", description="Пароль пользователя")
    is_admin: bool = Field(False)

class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""
    email: Optional[EmailStr] = Field(None, example="new@example.com", description="Новый email")
    password: Optional[str] = Field(None, min_length=6, example="newpassword", description="Новый пароль")


class UserOut(UserBase):
    """Схема для вывода данных пользователя."""
    id: int = Field(..., example=1, description="ID пользователя")

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Схема для аутентификации пользователя."""
    email: EmailStr = Field(..., example="user@example.com", description="Email пользователя")
    password: str = Field(..., min_length=6, example="strongpassword", description="Пароль пользователя")


class Token(BaseModel):
    """Схема JWT токена."""
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field("bearer", description="Тип токена")

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)

class TokenRefresh(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    message: str
