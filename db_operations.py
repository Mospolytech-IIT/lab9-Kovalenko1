from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, User, Post

DATABASE_URL = "postgresql+psycopg2://postgres:Crossfiri1@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def add_users():
    """Добавляет пользователей в базу данных."""
    session = SessionLocal()
    try:
        user1 = User(username="алиса", email="alisa@bk.com", password="pass1")
        user2 = User(username="боб", email="bob@bk.com", password="pass2")
        user3 = User(username="чарли", email="charlie@bk.com", password="pass3")

        session.add_all([user1, user2, user3])
        session.commit()
    finally:
        session.close()

def add_posts():
    """Добавляет посты в базу данных."""
    session = SessionLocal()
    try:
        post1 = Post(title="Первый пост Алисы", content="Привет от Алисы!", user_id=1)
        post2 = Post(title="Путешествие Боба", content="Я люблю путешествовать по миру!", user_id=2)
        post3 = Post(title="Мысли Чарли", content="Глубокие размышления...", user_id=3)

        session.add_all([post1, post2, post3])
        session.commit()
    finally:
        session.close()

def get_all_users():
    """Возвращает всех пользователей."""
    session = SessionLocal()
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

def get_all_posts_with_users():
    """Возвращает все посты вместе с информацией о пользователях."""
    session = SessionLocal()
    try:
        posts = session.query(Post).options(joinedload(Post.author)).all()
        return posts
    finally:
        session.close()

def get_posts_by_user(user_id):
    """Возвращает посты, принадлежащие определённому пользователю.

    Args:
        user_id (int): ID пользователя.

    Returns:
        List[Post]: Список постов пользователя.
    """
    session = SessionLocal()
    try:
        posts = session.query(Post).filter(Post.user_id == user_id).all()
        return posts
    finally:
        session.close()

def update_user_email(user_id, new_email):
    """Обновляет email пользователя.

    Args:
        user_id (int): ID пользователя.
        new_email (str): Новый email.
    """
    session = SessionLocal()
    try:
        session.execute(
            update(User).where(User.id == user_id).values(email=new_email)
        )
        session.commit()
    finally:
        session.close()

def update_post_content(post_id, new_content):
    """Обновляет содержимое поста.

    Args:
        post_id (int): ID поста.
        new_content (str): Новое содержимое.
    """
    session = SessionLocal()
    try:
        session.execute(
            update(Post).where(Post.id == post_id).values(content=new_content)
        )
        session.commit()
    finally:
        session.close()

def delete_post(post_id):
    """Удаляет пост по ID.

    Args:
        post_id (int): ID поста.
    """
    session = SessionLocal()
    try:
        session.execute(delete(Post).where(Post.id == post_id))
        session.commit()
    finally:
        session.close()

def delete_user_and_posts(user_id):
    """Удаляет пользователя и все его посты.

    Args:
        user_id (int): ID пользователя.
    """
    session = SessionLocal()
    try:
        session.execute(delete(Post).where(Post.user_id == user_id))
        session.execute(delete(User).where(User.id == user_id))
        session.commit()
    finally:
        session.close()

if __name__ == "__main__":
    # Пример использования:
    add_users()
    add_posts()

    print("Все пользователи:")
    for u in get_all_users():
        print(u.id, u.username, u.email)

    print("\nВсе посты с пользователями:")
    for p in get_all_posts_with_users():
        print(p.id, p.title, p.author.username)

    print("\nПосты пользователя с ID=1:")
    for p in get_posts_by_user(1):
        print(p.id, p.title)

    print("\nОбновление email пользователя:")
    update_user_email(1, "alisa_new@example.com")

    print("\nОбновление содержимого поста:")
    update_post_content(1, "Обновлённое содержимое первого поста Алисы")

    print("\nУдаление поста:")
    delete_post(2)

    print("\nУдаление пользователя и его постов:")
    delete_user_and_posts(3)
