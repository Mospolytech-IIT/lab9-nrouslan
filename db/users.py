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

def get_all_users(session):
    """Функция получения всех пользователей из БД."""
    return session.query(User).all()

def get_user_by_id(session, user_id):
    """Функция для получения пользователя по user_id."""
    return session.query(User).filter(User.id == user_id).all()[0]

def update_user_email(session, user_id, new_email):
    """Функция для обновления информации о пользователях в БД."""
    user = session.query(User).get(user_id)
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя {user.username} обновлен на {new_email}")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

def delete_user_and_posts(session, user_id):
    """Функция для удаления пользователя и его постов из БД."""
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} и его посты удалены.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")
