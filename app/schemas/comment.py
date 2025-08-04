from pydantic import BaseModel, Field
from typing import Optional
from .task import TaskOut
from .user import UserOut
from datetime import datetime


class CommentBase(BaseModel):
    """Базовая схема комментария."""
    text: str = Field(..., example="This is a comment", description="Текст комментария")


class CommentCreate(CommentBase):
    """Схема для создания комментария."""
    pass


class CommentUpdate(BaseModel):
    """Схема для обновления комментария."""
    text: Optional[str] = Field(None, example="Updated comment", description="Новый текст комментария")


class CommentOut(CommentBase):
    """Схема для вывода данных комментария."""
    id: int = Field(..., example=1, description="ID комментария")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00", description="Дата создания комментария")
    task_id: int = Field(..., example=1, description="ID задачи")
    author_id: int = Field(..., example=1, description="ID автора комментария")
    task: TaskOut = Field(..., description="Задача комментария")
    author: UserOut = Field(..., description="Автор комментария")

    class Config:
        from_attributes = True