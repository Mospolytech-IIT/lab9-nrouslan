"""Модуль с функцией для добавления пользователей в БД."""

from sqlalchemy.exc import IntegrityError

from db.models import User

def add_users(session, users):
    """Функция для добавления пользователей в БД."""
    for user_data in users:
        try:
            new_user = User(**user_data)
            session.add(new_user)
            session.commit()
            print(f"Пользователь {user_data['username']} добавлен.")
        except IntegrityError as e:
            session.rollback()
            print(f"Ошибка при добавлении пользователя {user_data['username']}: {e}")    
