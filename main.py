"""Модуль, реализующий FastAPI и SQLAlchemy."""

from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from db.models import Base
from db.models_pydantic import User, Post, CreateUserDto, UpdateUserDto
from db.users import add_users, get_all_users, get_user_by_id, update_user_email, delete_user_and_posts
from db.posts import add_posts, get_all_posts, get_posts_by_user, update_post_content, delete_post

app = FastAPI()
templates = Jinja2Templates(directory="templates")

engine = create_engine("sqlite:///users.db", echo=False)

try:
    Base.metadata.create_all(engine)
    print("Таблицы Users и Posts успешно созданы.")
except IntegrityError as e:
    print(f"Ошибка при создании таблиц: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    """Метод для получения контекста БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавление пользователей
users_to_add = [
    {'username': 'rusnik', 'email': 'rusnik@example.com', 'password': 'password1'},
    {'username': 'andfom', 'email': 'andfom@example.com', 'password': 'password2'},
    {'username': 'olepak', 'email': 'olepak@example.com', 'password': 'password3'},
]
add_users(session, users_to_add)

# Добавление постов
posts_to_add = [
    {'title': 'Post 1', 'content': 'Content 1', 'user_id': 1},
    {'title': 'Post 2', 'content': 'Content 2', 'user_id': 2},
    {'title': 'Post 3', 'content': 'Content 3', 'user_id': 1},
]
add_posts(session, posts_to_add)

session.close()

# --- Users endpoints ---

@app.get("/users")
def read_users(request: Request, db: Session = Depends(get_db)):
    """Эндпоинт для получения всех пользователей системы."""
    users = get_all_users(db)
    return templates.TemplateResponse("users/users.html", {"request": request, "users": users})

@app.get("/users/create")
def read_user_create(request: Request):
    """Эндпоинт для создания нового пользователя."""
    return templates.TemplateResponse("users/create_user.html", {"request": request})

@app.post("/users")
def create_user(user: CreateUserDto = Form(...), db: Session = Depends(get_db)):
    """Эндпоинт для сохранения нового пользователя."""
    add_users(db, [{'username': user.username, 'email': user.email, 'password': user.password}])
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

@app.get("/users/{user_id}/edit")
def read_user_edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Эндпоинт для обновления нового пользователя."""
    user = get_user_by_id(db, user_id)
    return templates.TemplateResponse("users/edit_user.html", {"request": request, "user": user})

@app.post("/users/{user_id}")
def update_user(user_id: int, user: UpdateUserDto = Form(...), db: Session = Depends(get_db)):
    """Эндпоинт для обновления почты пользователя."""
    update_user_email(db, user_id, user.email)
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

# --- Posts endpoints ---

@app.get("/posts")
def read_posts(request: Request, db: Session = Depends(get_db)):
    """Эндпоинт для получения всех постов системы."""
    posts = get_all_posts(db)
    return templates.TemplateResponse("posts/posts.html", {"request": request, "posts": posts})

# # Обновление данных
# update_user_email(session, 1, 'new_user1@example.com')
# update_post_content(session, 1, 'Updated content 1')

# # Удаление данных
# delete_post(session, 2)
# delete_user_and_posts(session, 2)
