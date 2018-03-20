from flask import Flask, request, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__, template_folder='templates')
app.config.from_object(config)

db = SQLAlchemy(app)


# Домашняя страница переводит сразу на гостевую книгу
@app.route('/')
def home():
    return redirect(url_for('index'))


# Посты гостевой книги
@app.route('/posts/', methods=['GET', 'POST'])
def index():
    from models import Post
    from forms import PostForm

    # Добавление поста
    if request.method == 'POST':
        form = PostForm(request.form)

        if form.validate():
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()

            flash('Пост опубликован.')

        else:
            flash('Форма не валидна! Пост не был опубликован.')

    posts = Post.query.all()

    # Вывод всех постов
    return render_template('show_posts.html', posts=posts)


# Маршрут для конкретного поста по его id
@app.route('/posts/<int:post_id>/', methods=['GET', 'POST'])
def show_post(post_id):
    from models import Comment, Post
    from forms import CommentForm

    # Получение определнного поста из базы данных по id из URL
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        return 'Not Found', 404

    # Добавление комментария
    if request.method == 'POST':
        form = CommentForm(request.form)

        if form.validate():
            comment = Comment(post=post, content=request.form['content'])
            db.session.add(comment)

            # Для поста увеличиваем переменную, хранящую количество комментариев
            post.number_of_comments += 1

            db.session.commit()

            flash('Комментарий опубликован.')

        else:
            flash('Форма не валидна! Комментарий не был опубликован.')

    # Получение всех комментариев из базы данных к текущему посту
    comments = Comment.query.filter_by(post_id=post.id).all()

    # Вывод поста и комментариев к нему
    return render_template('show_comments.html', post=post, comments=comments)


if __name__ == '__main__':
    from models import *

    db.create_all()
    app.run()
