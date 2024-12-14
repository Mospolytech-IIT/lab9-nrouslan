"""Модуль, реализующий FastAPI и SQLAlchemy."""

from fastapi import FastAPI, Depends, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from db.models import Base
from db.models_pydantic import CreateUserDto, CreatePostDto, \
    UpdateUserDto, UpdatePostDto
from db.users import add_users, get_all_users, \
    get_user_by_id, update_user_email, \
    delete_user_and_posts
from db.posts import add_posts, get_all_posts, \
    get_post_by_id, update_post_content, \
    delete_post

app = FastAPI()
templates = Jinja2Templates(directory="templates")
engine = create_engine("sqlite:///users.db", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def populate_db():
    """Метод для первоначального заполнения БД данными."""

    try:
        Base.metadata.create_all(engine)
        print("---> Таблицы Users и Posts успешно созданы.")

        if len(get_all_users(session)) == 0:
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
        else:
            print("--> БД уже заполнена начальными данными...")  
    except IntegrityError as e:
        print(f"---> Ошибка при создании таблиц: {e}")

def get_db():
    """Метод для получения контекста БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

populate_db()

session.close()

@app.get("/")
def read_root():
    """Корневой эндпоинт для редиректа на списко пользователей."""
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

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
def create_user(create_user_dto: CreateUserDto = Form(...), db: Session = Depends(get_db)):
    """Эндпоинт для сохранения нового пользователя."""
    add_users(db, [
        {
            'username': create_user_dto.username,
            'email': create_user_dto.email, 
            'password': create_user_dto.password
        }
    ])
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

@app.get("/users/{user_id}/edit")
def read_user_edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    """Эндпоинт для обновления данных пользователя."""
    user = get_user_by_id(db, user_id)
    return templates.TemplateResponse("users/edit_user.html", {"request": request, "user": user})

@app.post("/users/{user_id}")
def update_user(
    user_id: int,
    update_user_dto: UpdateUserDto = Form(...), db: Session = Depends(get_db)
):
    """Эндпоинт для обновления почты пользователя."""
    update_user_email(db, user_id, update_user_dto.email)
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

@app.post("/users/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Эндпоинт для удаления пользователя и его постов."""
    delete_user_and_posts(db, user_id)
    return RedirectResponse("/users", status_code=status.HTTP_302_FOUND)

# --- Posts endpoints ---

@app.get("/posts")
def read_posts(request: Request, db: Session = Depends(get_db)):
    """Эндпоинт для получения всех постов системы."""
    posts = get_all_posts(db)
    return templates.TemplateResponse("posts/posts.html", {"request": request, "posts": posts})

@app.get("/posts/create")
def read_post_create(request: Request, db: Session = Depends(get_db)):
    """Эндпоинт для создания нового поста."""
    users = get_all_users(db)
    return templates.TemplateResponse(
        "posts/create_post.html", 
        {"request": request, "users": users})

@app.post("/posts")
def create_post(create_post_dto: CreatePostDto = Form(...), db: Session = Depends(get_db)):
    """Эндпоинт для создания нового поста."""
    add_posts(db, [
        {
            'title': create_post_dto.title, 
            'content': create_post_dto.content, 
            'user_id': create_post_dto.user_id
        }])
    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)

@app.get("/posts/{post_id}/edit")
def read_post_edit(request: Request, post_id: int, db: Session = Depends(get_db)):
    """Эндпоинт для обновления данных поста."""
    post = get_post_by_id(db, post_id)
    return templates.TemplateResponse("posts/edit_post.html", {"request": request, "post": post})

@app.post("/posts/{post_id}")
def update_post(
    post_id: int,
    update_post_dto: UpdatePostDto = Form(...), db: Session = Depends(get_db)
):
    """Эндпоинт для обновления контента поста."""
    update_post_content(db, post_id, update_post_dto.content)
    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)

@app.post("/posts/{post_id}/delete")
def delete_post_route(post_id: int, db: Session = Depends(get_db)):
    """Эндпоинт для удаления поста пользователя."""
    delete_post(db, post_id)
    return RedirectResponse("/posts", status_code=status.HTTP_302_FOUND)
