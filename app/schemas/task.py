from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from .project import ProjectOut
from datetime import datetime


class TaskStatus(str, Enum):
    """Статусы задачи."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class TaskBase(BaseModel):
    """Базовая схема задачи."""
    title: str = Field(..., max_length=100, example="Implement feature", description="Название задачи")
    status: TaskStatus = Field(TaskStatus.TODO, example="todo", description="Статус задачи")


class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи."""
    title: Optional[str] = Field(None, max_length=100, example="Updated task", description="Новое название задачи")
    status: Optional[TaskStatus] = Field(None, example="in_progress", description="Новый статус задачи")


class TaskOut(TaskBase):
    """Схема для вывода данных задачи."""
    id: int = Field(..., example=1, description="ID задачи")
    project_id: int = Field(..., example=1, description="ID проекта")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00", description="Дата создания задачи")
    project: ProjectOut = Field(..., description="Проект задачи")

    class Config:
        from_attributes = True