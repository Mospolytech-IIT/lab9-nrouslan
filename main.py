"""Модуль, реализующий FastAPI и SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.users import add_users
from db.models import Base

engine = create_engine("sqlite:///users.db", echo=True)

try:
    Base.metadata.create_all(engine)
    print("Таблицы Users и Posts успешно созданы.")
except Exception as e:
    print(f"Ошибка при создании таблиц: {e}")

Session = sessionmaker(bind=engine)
session = Session()

# Добавление пользователей
users_to_add = [
    {'username': 'rusnik', 'email': 'rusnik@example.com', 'password': 'password1'},
    {'username': 'andfom', 'email': 'andfom@example.com', 'password': 'password2'},
    {'username': 'olepak', 'email': 'olepak@example.com', 'password': 'password3'},
]
add_users(session, users_to_add)

session.close()
