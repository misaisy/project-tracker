from pydantic import BaseModel, Field
from typing import Optional
from .user import UserOut
from datetime import datetime


class ProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: str = Field(..., max_length=100, example="My Project", description="Название проекта")
    description: Optional[str] = Field(None, example="Project description", description="Описание проекта")


class ProjectCreate(ProjectBase):
    """Схема для создания проекта."""
    pass


class ProjectUpdate(BaseModel):
    """Схема для обновления проекта."""
    name: Optional[str] = Field(None, max_length=100, example="Updated Project", description="Новое название проекта")
    description: Optional[str] = Field(None, example="Updated description", description="Новое описание проекта")


class ProjectOut(ProjectBase):
    """Схема для вывода данных проекта."""
    id: int = Field(..., example=1, description="ID проекта")
    owner_id: int = Field(..., example=1, description="ID владельца проекта")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00", description="Дата создания проекта")
    owner: UserOut = Field(..., description="Владелец проекта")

    class Config:
        from_attributes = True