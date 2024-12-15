from typing import List
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post

DATABASE_URL = "postgresql+psycopg2://postgres:Crossfiri1@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

HTML_TEMPLATE_USERS = """
<h1>Пользователи</h1>
<form action="/users/create" method="post">
    Имя пользователя: <input name="username"><br>
    Электронная почта: <input name="email"><br>
    Пароль: <input name="password" type="password"><br>
    <input type="submit" value="Создать пользователя">
</form>
<ul>
{items}
</ul>
"""

HTML_TEMPLATE_POSTS = """
<h1>Посты</h1>
<form action="/posts/create" method="post">
    Заголовок: <input name="title"><br>
    Содержимое: <input name="content"><br>
    ID пользователя: <input name="user_id" type="number"><br>
    <input type="submit" value="Создать пост">
</form>
<ul>
{items}
</ul>
"""

HTML_TEMPLATE_EDIT_USER = """
<h1>Редактировать пользователя</h1>
<form action="/users/edit/{user_id}" method="post">
    Имя пользователя: <input name="username" value="{username}"><br>
    Электронная почта: <input name="email" value="{email}"><br>
    Пароль: <input name="password" value="{password}" type="password"><br>
    <input type="submit" value="Обновить пользователя">
</form>
"""

HTML_TEMPLATE_EDIT_POST = """
<h1>Редактировать пост</h1>
<form action="/posts/edit/{post_id}" method="post">
    Заголовок: <input name="title" value="{title}"><br>
    Содержимое: <input name="content" value="{content}"><br>
    ID пользователя: <input name="user_id" type="number" value="{user_id}"><br>
    <input type="submit" value="Обновить пост">
</form>
"""

@app.get("/users", response_class=HTMLResponse)
def list_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        items = ""
        for u in users:
            items += f"<li>{u.username} ({u.email}) <a href='/users/edit/{u.id}'>Редактировать</a> <a href='/users/delete/{u.id}'>Удалить</a></li>"
        return HTML_TEMPLATE_USERS.format(items=items)
    finally:
        session.close()

@app.post("/users/create", response_class=HTMLResponse)
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    session = SessionLocal()
    try:
        new_user = User(username=username, email=email, password=password)
        session.add(new_user)
        session.commit()
        return "<p>Пользователь создан</p><a href='/users'>Назад</a>"
    finally:
        session.close()

@app.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user_form(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return HTML_TEMPLATE_EDIT_USER.format(user_id=user.id, username=user.username, email=user.email, password=user.password)
    finally:
        session.close()

@app.post("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user(user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        user.username = username
        user.email = email
        user.password = password
        session.commit()
        return "<p>Пользователь обновлён</p><a href='/users'>Назад</a>"
    finally:
        session.close()

@app.get("/users/delete/{user_id}", response_class=HTMLResponse)
def delete_user(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
        return "<p>Пользователь и его посты удалены</p><a href='/users'>Назад</a>"
    finally:
        session.close()

@app.get("/posts", response_class=HTMLResponse)
def list_posts():
    session = SessionLocal()
    try:
        posts = session.query(Post).all()
        items = ""
        for p in posts:
            items += f"<li>{p.title} от пользователя {p.user_id} <a href='/posts/edit/{p.id}'>Редактировать</a> <a href='/posts/delete/{p.id}'>Удалить</a></li>"
        return HTML_TEMPLATE_POSTS.format(items=items)
    finally:
        session.close()

@app.post("/posts/create", response_class=HTMLResponse)
def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    session = SessionLocal()
    try:
        new_post = Post(title=title, content=content, user_id=user_id)
        session.add(new_post)
        session.commit()
        return "<p>Пост создан</p><a href='/posts'>Назад</a>"
    finally:
        session.close()

@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post_form(post_id: int):
    session = SessionLocal()
    try:
        post = session.query(Post).get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        return HTML_TEMPLATE_EDIT_POST.format(post_id=post.id, title=post.title, content=post.content, user_id=post.user_id)
    finally:
        session.close()

@app.post("/posts/edit/{post_id}", response_class=HTMLResponse)
def edit_post(post_id: int, title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    session = SessionLocal()
    try:
        post = session.query(Post).get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        post.title = title
        post.content = content
        post.user_id = user_id
        session.commit()
        return "<p>Пост обновлён</p><a href='/posts'>Назад</a>"
    finally:
        session.close()

@app.get("/posts/delete/{post_id}", response_class=HTMLResponse)
def delete_post(post_id: int):
    session = SessionLocal()
    try:
        post = session.query(Post).get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Пост не найден")
        session.delete(post)
        session.commit()
        return "<p>Пост удалён</p><a href='/posts'>Назад</a>"
    finally:
        session.close()
