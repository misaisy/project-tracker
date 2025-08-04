"""Пакет с операциями CRUD для всех сущностей приложения."""
from .user import get_user, get_user_by_email, create_user, update_user, delete_user
from .project import (
    create_project,
    get_project,
    get_user_projects,
    update_project,
    delete_project
)
from .task import (
    create_task,
    get_task,
    get_project_tasks,
    update_task,
    delete_task
)
from .comment import (
    create_comment,
    get_comment,
    get_task_comments,
    update_comment,
    delete_comment
)

__all__ = [
    'get_user',
    'get_user_by_email',
    'create_user',
    'update_user',
    'delete_user',
    'create_project',
    'get_project',
    'get_user_projects',
    'update_project',
    'delete_project',
    'create_task',
    'get_task',
    'get_project_tasks',
    'update_task',
    'delete_task',
    'create_comment',
    'get_comment',
    'get_task_comments',
    'update_comment',
    'delete_comment'
]