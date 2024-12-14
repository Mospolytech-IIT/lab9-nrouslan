"""Модуль с функцией для добавления постов в БД."""

from sqlalchemy.exc import IntegrityError

from db.models import Post

def add_posts(session, posts):
    """Функция для добавления постов в БД."""
    for post_data in posts:
        try:
            new_post = Post(**post_data)
            session.add(new_post)
            session.commit()
            print(f"Пост '{post_data['title']}' добавлен.")
        except IntegrityError as e:
            session.rollback()
            print(f"Ошибка при добавлении поста '{post_data['title']}': {e}")

def get_all_posts(session):
    """Функция для получения всех постов из БД."""
    return session.query(Post).all()

def get_posts_by_user(session, user_id):
    """Функция для получения всех постов пользователя из БД."""
    return session.query(Post).filter(Post.user_id == user_id).all()

def get_post_by_id(session, post_id):
    """Функция для получения пользователя из БД по id."""
    return session.query(Post).filter(Post.id == post_id).all()[0]

def update_post_content(session, post_id, new_content):
    """Функция для обновления содержимого поста в БД."""
    post = session.query(Post).get(post_id)
    if post:
        post.content = new_content
        session.commit()
        print(f"Контент поста с ID {post_id} обновлен.")
    else:
        print(f"Пост с ID {post_id} не найден.")

def delete_post(session, post_id):
    """Функция для удаления поста из БД."""
    post = session.query(Post).get(post_id)
    if post:
        session.delete(post)
        session.commit()
        print(f"Пост с ID {post_id} удален.")
    else:
        print(f"Пост с ID {post_id} не найден.")
