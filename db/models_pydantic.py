"""Модуль с моделями пользователей и постов."""

from typing import List

from pydantic import BaseModel, Field

class User(BaseModel):
    """Модель пользователя."""
    id: int = Field(..., ge=1)
    username: str
    email: str
    password: str

class UserList(BaseModel):
    """Модель списка пользователей."""
    users: List[User]
    
class CreateUserDto(BaseModel):
    """Dto-объект для создания нового пользователя."""
    username: str
    email: str
    password: str

class UpdateUserDto(BaseModel):
    """Dto-объект для обновления данных пользователя."""
    email: str

class Post(BaseModel):
    """Модель поста."""
    id: int = Field(..., ge=1)
    title: str
    content: str
    user_id: int

class PostList(BaseModel):
    """Модель списка постов."""
    posts: List[Post]
